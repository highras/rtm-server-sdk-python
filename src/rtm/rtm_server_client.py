#encoding=utf8

import sys
sys.path.append("..")
import threading
import hashlib
import copy
import random
from .rtm_server_config import *
from .rtm_callback_internal import *
from .rtm_quest_processor_internal import *
from .rtm_server_structures import *

class RTMServerClient(object):
    error_recorder = RTMServerConfig.ERROR_RECORDER

    class RegressiveStatus(object):
        def __init__(self):
            self.connect_failed_count = 0
            self.regressive_connect_interval = RegressiveStrategy.first_interval_seconds

    def __init__(self, pid, secret, endpoint):
        self.stop = False
        self.pid = pid
        self.secret = secret
        arr = endpoint.split(':')
        self.auto_reconnect = True
        self.connect_callback = None
        self.client = TCPClient(arr[0], int(arr[1]))
        self.client.set_quest_timeout(RTMServerConfig.GLOBAL_QUEST_TIMEOUT_SECONDS * 1000)
        self.client.set_connect_timeout(RTMServerConfig.GLOBAL_CONNECT_TIMEOUT_SECONDS * 1000)
        self.config_callback()
        self.seq_lock = threading.Lock()
        self.seq = 0
        self.rand_id = random.randint(1, 255)
        self.rand_bits = 8
        self.seq_bits = 6
        self.seq_mask = -1 ^ (-1 << self.seq_bits)
        self.last_time = 0
        self.client.set_error_recorder(self.error_recorder)
        self.processor = None
        self.is_reconnect = False
        self.can_reconnect = False
        self.last_connect_time = 0
        self.last_close_time = 0
        self.require_close = False
        self.file_gate_lock = threading.Lock()
        self.file_gate_dict = {}
        self.check_thread = threading.Thread(target=RTMServerClient.check, args=(self,))
        self.check_thread.setDaemon(True)
        self.check_thread.start()
        self.reconnect_lock = threading.Lock()
        self.listen_status_info = ListenStatusInfo()
        self.regressive_strategy = RegressiveStrategy()
        self.regressive_status = RTMServerClient.RegressiveStatus()
        self.listen_lock = threading.Lock()
        

    def set_auto_connect(self, auto_connect):
        self.auto_reconnect = auto_connect
        self.client.set_auto_connect(auto_connect)

    def set_regressive_strategy(self, strategy):
        self.regressive_strategy = strategy
        self.regressive_status.regressive_connect_interval = self.regressive_strategy.first_interval_seconds

    def set_quest_timeout(self, timeout):
        self.client.set_quest_timeout(timeout * 1000)

    def set_connect_timeout(self, timeout):
        self.client.set_connect_timeout(timeout * 1000)

    def set_connection_callback(self, callback):
        self.connect_callback = callback

    def enable_encryptor_by_pem_file(self, pem_pub_file, curve_name = 'secp256k1', strength = 128):
        self.client.enable_encryptor_by_pem_file(pem_pub_file, curve_name, strength)

    def set_quest_processor(self, processor):
        if self.processor == None:
            self.processor = RtmQuestProcessorInternal()
        self.processor.set_processor(processor)
        self.client.set_quest_processor(self.processor)

    def set_error_recorder(self, recorder):
        self.error_recorder = recorder
        self.client.set_error_recorder(recorder)    

    def config_callback(self):
        class RTMConnectCallbackInternal(ConnectionCallback):
            def __init__(self, client):
                self.client = client

            def connected(self, connection_id, endpoint, connected):
                with self.client.reconnect_lock:
                    if connected:
                        self.client.can_reconnect = True
                        self.client.last_connect_time = int(time.time()*1000.0)

                    if connected and self.client.is_reconnect:
                        self.client.listen_status_restoration()

                    if self.client.connect_callback != None:
                        self.client.connect_callback.connected(connection_id, endpoint, connected, self.client.is_reconnect)

                    if not connected and self.client.can_reconnect:
                        self.client.try_reconnect()

            def closed(self, connection_id, endpoint, caused_by_error):
                with self.client.reconnect_lock:
                    self.client.last_close_time = int(time.time()*1000.0)

                    if self.client.connect_callback != None:
                        self.client.connect_callback.closed(connection_id, endpoint, caused_by_error, self.client.is_reconnect)

                    if not self.client.require_close and self.client.auto_reconnect:
                        self.client.is_reconnect = True
                        if self.client.last_close_time - self.client.last_connect_time > self.client.regressive_strategy.connect_failed_max_interval_milliseconds:
                            self.client.regressive_status.connect_failed_count = 0
                            self.client.regressive_status.regressive_connect_interval = self.client.regressive_strategy.first_interval_seconds
                        self.client.try_reconnect()
        self.client.set_connection_callback(RTMConnectCallbackInternal(self))

    def listen_status_restoration(self):
        class MySetListenCallback(BasicCallback):
            def callback(self, error_code):
                if error_code != FPNN_ERROR.FPNN_EC_OK and RTMServerClient.error_recorder != None:
                    RTMServerClient.error_recorder.record_error("set_listen after reconnect error, code: " + str(error_code))

        if self.listen_status_info.all_p2p or self.listen_status_info.all_groups or self.listen_status_info.all_rooms or self.listen_status_info.all_events:
            self.set_all_listen(self.listen_status_info.all_p2p, self.listen_status_info.all_groups, self.listen_status_info.all_rooms, self.listen_status_info.all_events, MySetListenCallback())

        if len(self.listen_status_info.user_ids) > 0 or len(self.listen_status_info.group_ids) > 0 or len(self.listen_status_info.room_ids) > 0 or len(self.listen_status_info.events) > 0:
            self.set_listen(self.listen_status_info.group_ids, self.listen_status_info.room_ids, self.listen_status_info.user_ids, self.listen_status_info.events, MySetListenCallback())

    def try_reconnect(self):
        if self.regressive_status.connect_failed_count < self.regressive_strategy.start_connect_failed_count:
            self.regressive_status.connect_failed_count += 1
            self.client.reconnect()
        else:
            self.client.engine.thread_pool_execute(self.regressive_reconnect, ())

    def regressive_reconnect(self):
        sleep_interval = 0
        with self.reconnect_lock:
            sleep_interval = self.regressive_status.regressive_connect_interval
            self.regressive_status.regressive_connect_interval += (self.regressive_strategy.max_interval_seconds - self.regressive_strategy.first_interval_seconds) / self.regressive_strategy.linear_regressive_count
        time.sleep(sleep_interval)
        with self.reconnect_lock:
            self.regressive_status.connect_failed_count += 1
            self.client.reconnect()

    def close(self):
        self.require_close = True
        self.client.close()

    def reconnect(self):
        self.client.reconnect()

    def destory(self):
        self.require_close = True
        self.stop = True
        self.client.destory()

    def get_next_millis(self):
        t = int(time.time()*1000)
        while t <= self.last_time:
            t = int(time.time()*1000)
        return t

    def gen_mid(self):
        with self.seq_lock:
            self.seq += 1
            t = int(time.time()*1000)
            self.seq = (self.seq+1) & self.seq_mask
            if self.seq == 0:
                t = self.get_next_millis()
            self.last_time = t
            return (t << (self.rand_bits + self.seq_bits)) | (self.rand_id << self.seq_bits)

    def gen_sign(self, salt, cmd, ts):
        return hashlib.md5((str(self.pid) + ':' + self.secret + ':' +
                str(salt) + ':' + cmd + ':' + str(ts)).encode('utf-8')).hexdigest().upper()


    def get_token(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetTokenCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('gettoken', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'gettoken', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'version' : 'PYTHON-' + RTM_SDK_VERSION
        })
        callback_internal = GetTokenCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def kickout(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('kickout', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'kickout', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def add_device(self, uid, app_type, device_token, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('adddevice', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'adddevice', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'apptype' : app_type,
            'devicetoken' : device_token
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def remove_device(self, uid, device_token, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('removedevice', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'removedevice', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'devicetoken' : device_token
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def add_device_push_option(self, uid, option_type, xid, mtypes = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('addoption', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'addoption', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'type' : option_type,
            'xid' : xid
        })
        if (mtypes != None):
            quest.param('mtypes', mtypes)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def remove_device_push_option(self, uid, option_type, xid, mtypes = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('removeoption', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'removeoption', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'type' : option_type,
            'xid' : xid
        })
        if (mtypes != None):
            quest.param('mtypes', mtypes)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_device_push_option(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetDevicePushOptionCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getoption', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getoption', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        callback_internal = GetDevicePushOptionCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def remove_token(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('removetoken', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'removetoken', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def send_message(self, mtype, from_uid, to_uid, message, attrs, mid = 0, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendMessageCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        if mid == 0:
            mid = self.gen_mid()
        quest = Quest('sendmsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'sendmsg', ts),
            'salt' : salt,
            'ts' : ts,
            'mtype' : mtype,
            'from' : from_uid,
            'to' : to_uid,
            'mid' : mid,
            'msg' : message,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def send_messages(self, mtype, from_uid, to_uids, message, attrs, mid = 0, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendMessageCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        if mid == 0:
            mid = self.gen_mid()
        quest = Quest('sendmsgs', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'sendmsgs', ts),
            'salt' : salt,
            'ts' : ts,
            'mtype' : mtype,
            'from' : from_uid,
            'tos' : to_uids,
            'mid' : mid,
            'msg' : message,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def send_group_message(self, mtype, from_uid, gid, message, attrs, mid = 0, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendMessageCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        if mid == 0:
            mid = self.gen_mid()
        quest = Quest('sendgroupmsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'sendgroupmsg', ts),
            'salt' : salt,
            'ts' : ts,
            'mtype' : mtype,
            'from' : from_uid,
            'gid' : gid,
            'mid' : mid,
            'msg' : message,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def send_room_message(self, mtype, from_uid, rid, message, attrs, mid = 0, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendMessageCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        if mid == 0:
            mid = self.gen_mid()
        quest = Quest('sendroommsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'sendroommsg', ts),
            'salt' : salt,
            'ts' : ts,
            'mtype' : mtype,
            'from' : from_uid,
            'rid' : rid,
            'mid' : mid,
            'msg' : message,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def broadcast_message(self, mtype, from_uid, message, attrs, mid = 0, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendMessageCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        if mid == 0:
            mid = self.gen_mid()
        quest = Quest('broadcastmsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'broadcastmsg', ts),
            'salt' : salt,
            'ts' : ts,
            'mtype' : mtype,
            'from' : from_uid,
            'mid' : mid,
            'msg' : message,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_group_message(self, uid, gid, desc, num, begin = None, end = None, lastid = None, mtypes = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetGroupMessageCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getgroupmsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getgroupmsg', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'gid' : gid,
            'desc' : desc,
            'num' : num
        })
        if begin != None:
            quest.param('begin', begin)
        if end != None:
            quest.param('end', end)
        if lastid != None:
            quest.param('lastid', lastid)
        if mtypes != None:
            quest.param('mtypes', mtypes)
        callback_internal = GetGroupMessageCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_room_message(self, uid, rid, desc, num, begin = None, end = None, lastid = None, mtypes = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetRoomMessageCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getroommsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getroommsg', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'rid' : rid,
            'desc' : desc,
            'num' : num
        })
        if begin != None:
            quest.param('begin', begin)
        if end != None:
            quest.param('end', end)
        if lastid != None:
            quest.param('lastid', lastid)
        if mtypes != None:
            quest.param('mtypes', mtypes)
        callback_internal = GetRoomMessageCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_broadcast_message(self, uid, desc, num, begin = None, end = None, lastid = None, mtypes = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetBroadcastMessageCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getbroadcastmsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getbroadcastmsg', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'desc' : desc,
            'num' : num
        })
        if begin != None:
            quest.param('begin', begin)
        if end != None:
            quest.param('end', end)
        if lastid != None:
            quest.param('lastid', lastid)
        if mtypes != None:
            quest.param('mtypes', mtypes)
        callback_internal = GetBroadcastMessageCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_p2p_message(self, uid, ouid, desc, num, begin = None, end = None, lastid = None, mtypes = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetP2PMessageCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getp2pmsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getp2pmsg', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'ouid' : ouid,
            'desc' : desc,
            'num' : num
        })
        if begin != None:
            quest.param('begin', begin)
        if end != None:
            quest.param('end', end)
        if lastid != None:
            quest.param('lastid', lastid)
        if mtypes != None:
            quest.param('mtypes', mtypes)
        callback_internal = GetP2PMessageCallbackInternal(uid, ouid, callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def delete_message(self, mid, from_uid, xid, mtype, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('delmsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'delmsg', ts),
            'salt' : salt,
            'ts' : ts,
            'mid' : mid,
            'from' : from_uid,
            'xid' : xid,
            'type' : mtype
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def delete_p2p_message(self, mid, from_uid, to_uid, callback = None, timeout = 0):
        return self.delete_message(mid, from_uid, to_uid, MessageType.P2P_MESSAGE.value, callback, timeout)

    def delete_group_message(self, mid, from_uid, gid, callback = None, timeout = 0):
        return self.delete_message(mid, from_uid, gid, MessageType.GROUP_MESSAGE.value, callback, timeout)

    def delete_room_message(self, mid, from_uid, rid, callback = None, timeout = 0):
        return self.delete_message(mid, from_uid, rid, MessageType.ROOM_MESSAGE.value, callback, timeout)

    def delete_broadcast_message(self, mid, from_uid, callback = None, timeout = 0):
        return self.delete_message(mid, from_uid, 0, MessageType.BROADCAST_MESSAGE.value, callback, timeout)

    def get_message_info(self, mid, from_uid, xid, mtype, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetMessageInfoCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getmsg', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getmsg', ts),
            'salt' : salt,
            'ts' : ts,
            'mid' : mid,
            'from' : from_uid,
            'xid' : xid,
            'type' : mtype
        })
        callback_internal = GetMessageInfoCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_p2p_message_info(self, mid, from_uid, to_uid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, to_uid, MessageType.P2P_MESSAGE.value, callback, timeout)

    def get_group_message_info(self, mid, from_uid, gid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, gid, MessageType.GROUP_MESSAGE.value, callback, timeout)

    def get_room_message_info(self, mid, from_uid, rid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, rid, MessageType.ROOM_MESSAGE.value, callback, timeout)

    def get_broadcast_message_info(self, mid, from_uid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, 0, MessageType.BROADCAST_MESSAGE.value, callback, timeout)

    def send_chat(self, from_uid, to_uid, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_message(ChatMessageType.TEXT.value, from_uid, to_uid, message, attrs, mid, callback, timeout)

    def send_chats(self, from_uid, to_uids, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_messages(ChatMessageType.TEXT.value, from_uid, to_uids, message, attrs, mid, callback, timeout)

    def send_group_chat(self, from_uid, gid, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_group_message(ChatMessageType.TEXT.value, from_uid, gid, message, attrs, mid, callback, timeout)

    def send_room_chat(self, from_uid, rid, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_room_message(ChatMessageType.TEXT.value, from_uid, rid, message, attrs, mid, callback, timeout)

    def broadcast_chat(self, from_uid, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.broadcast_message(ChatMessageType.TEXT.value, from_uid, message, attrs, mid, callback, timeout)

    def send_cmd(self, from_uid, to_uid, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_message(ChatMessageType.CMD.value, from_uid, to_uid, message, attrs, mid, callback, timeout)

    def send_cmds(self, from_uid, to_uids, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_messages(ChatMessageType.CMD.value, from_uid, to_uids, message, attrs, mid, callback, timeout)

    def send_group_cmd(self, from_uid, gid, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_group_message(ChatMessageType.CMD.value, from_uid, gid, message, attrs, mid, callback, timeout)

    def send_room_cmd(self, from_uid, rid, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_room_message(ChatMessageType.CMD.value, from_uid, rid, message, attrs, mid, callback, timeout)

    def broadcast_cmd(self, from_uid, message, attrs, mid = 0, callback = None, timeout = 0):
        return self.broadcast_message(ChatMessageType.CMD.value, from_uid, message, attrs, mid, callback, timeout)

    def get_group_chat(self, uid, gid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0):
        return self.get_group_message(uid, gid, desc, num, begin, end, lastid, [ChatMessageType.TEXT.value, ChatMessageType.CMD.value], callback, timeout)

    def get_room_chat(self, uid, rid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0):
        return self.get_room_message(uid, rid, desc, num, begin, end, lastid, [ChatMessageType.TEXT.value, ChatMessageType.CMD.value], callback, timeout)

    def get_broadcast_chat(self, uid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0):
        return self.get_broadcast_message(uid, desc, num, begin, end, lastid, [ChatMessageType.TEXT.value, ChatMessageType.CMD.value], callback, timeout)

    def get_p2p_chat(self, uid, ouid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0):
        return self.get_p2p_message(uid, ouid, desc, num, begin, end, lastid, [ChatMessageType.TEXT.value, ChatMessageType.CMD.value], callback, timeout)

    def delete_p2p_chat(self, mid, from_uid, to_uid, callback = None, timeout = 0):
        return self.delete_message(mid, from_uid, to_uid, MessageType.P2P_MESSAGE.value, callback, timeout)

    def delete_group_chat(self, mid, from_uid, gid, callback = None, timeout = 0):
        return self.delete_message(mid, from_uid, gid, MessageType.GROUP_MESSAGE.value, callback, timeout)

    def delete_room_chat(self, mid, from_uid, rid, callback = None, timeout = 0):
        return self.delete_message(mid, from_uid, rid, MessageType.ROOM_MESSAGE.value, callback, timeout)

    def delete_broadcast_chat(self, mid, from_uid, callback = None, timeout = 0):
        return self.delete_message(mid, from_uid, 0, MessageType.BROADCAST_MESSAGE.value, callback, timeout)

    def get_p2p_chat_info(self, mid, from_uid, to, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, to, MessageType.P2P_MESSAGE.value, callback, timeout)

    def get_group_chat_info(self, mid, from_uid, gid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, gid, MessageType.GROUP_MESSAGE.value, callback, timeout)

    def get_room_chat_info(self, mid, from_uid, rid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, rid, MessageType.ROOM_MESSAGE.value, callback, timeout)

    def get_broadcast_chat_info(self, mid, from_uid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, 0, MessageType.BROADCAST_MESSAGE.value, callback, timeout)

    def translate(self, text, dst, src = None, ttype = 'chat', profanity = 'off', uid = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, TranslateCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('translate', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'translate', ts),
            'salt' : salt,
            'ts' : ts,
            'text' : text,
            'dst' : dst,
            'type' : ttype,
            'profanity' : profanity
        })
        if src != None:
            quest.param('src', src)
        if uid != None:
            quest.param('uid', uid)
        callback_internal = TranslateCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def text_check(self, text, uid = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, TextCheckCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('tcheck', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'tcheck', ts),
            'salt' : salt,
            'ts' : ts,
            'text' : text
        })
        if uid != None:
            quest.param('uid', uid)
        callback_internal = TextCheckCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def image_check(self, image, image_type, uid = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, CheckCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('icheck', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'icheck', ts),
            'salt' : salt,
            'ts' : ts,
            'image' : image,
            'type' : image_type
        })
        if uid != None:
            quest.param('uid', uid)
        callback_internal = CheckCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def audio_check(self, audio, audio_type, lang, codec = None, srate = None, uid = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, CheckCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('acheck', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'acheck', ts),
            'salt' : salt,
            'ts' : ts,
            'audio' : audio,
            'type' : audio_type,
            'lang' : lang
        })
        if codec != None:
            quest.param('codec', codec)
        if srate != None:
            quest.param('srate', srate)
        if uid != None:
            quest.param('uid', uid)
        callback_internal = CheckCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def video_check(self, video, video_type, video_name, uid = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, CheckCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('vcheck', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'vcheck', ts),
            'salt' : salt,
            'ts' : ts,
            'video' : video,
            'type' : video_type,
            'videoName' : video_name
        })
        if uid != None:
            quest.param('uid', uid)
        callback_internal = CheckCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def speech_to_text(self, audio, audio_type, lang, codec = None, srate = None, uid = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SpeechToTextCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('speech2text', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'speech2text', ts),
            'salt' : salt,
            'ts' : ts,
            'audio' : audio,
            'type' : audio_type,
            'lang' : lang
        })
        if codec != None:
            quest.param('codec', codec)
        if srate != None:
            quest.param('srate', srate)
        if uid != None:
            quest.param('uid', uid)
        callback_internal = SpeechToTextCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def file_token(self, from_uid, cmd, to_uids = None, to_uid = None, rid = None, gid = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, FileTokenCallback):
            raise Exception('callback type error')
        if cmd not in ['sendfile', 'sendfiles', 'sendroomfile', 'sendgroupfile', 'broadcastfile']:
            raise Exception('cmd is wrong')
        if cmd != 'broadcastfile' and to_uids == None and to_uid == None and rid == None and gid == None:
            raise Exception('to_uids/to_uid/rid/gid must exist one')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('filetoken', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'filetoken', ts),
            'salt' : salt,
            'ts' : ts,
            'from' : from_uid,
            'cmd' : cmd
        })
        if to_uids != None:
            quest.param('tos', to_uids)
        if to_uid != None:
            quest.param('to', to_uid)
        if rid != None:
            quest.param('rid', rid)
        if gid != None:
            quest.param('gid', gid)
        callback_internal = FileTokenCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def check(self):
        while not self.stop:
            time.sleep(1)
            now = time.time()
            with self.file_gate_lock:
                for (endpoint, client_info) in  self.file_gate_dict.items(): 
                    if now - client_info.update_time >= RTMServerConfig.FILE_GATE_CLIENT_HOLDING_SECONDS:
                        client_info.client.close()
                        del self.file_gate_dict[endpoint]

    class FileGateInfo(object):
        def __init__(self, client):
            self.update_time = time.time()
            self.client = client

    class SendFileInfo(object):
        def __init__(self, timeout):
            if timeout > 0:
                self.remain_timeout = timeout * 1000
            else:
                self.remain_timeout = RTMServerConfig.GLOBAL_QUEST_TIMEOUT_SECONDS * 1000
            self.send_type = ''
            self.from_uid = 0
            self.mtype = 0
            self.file_path = ''
            self.file_content = ''
            self.token = ''
            self.to_id = 0
            self.to_ids = []

    def fetch_file_client(self, endpoint, send_file_info):
        client_info = None
        with self.file_gate_lock:
            client_info = self.file_gate_dict.get(endpoint, None)
        if client_info != None:
            return client_info

        arr = endpoint.split(':')
        client = TCPClient(arr[0], int(arr[1]))
        client.set_connect_timeout(send_file_info.remain_timeout)
        client.set_error_recorder(self.error_recorder)
        
        class FielGateConnectCallbackInternal(ConnectionCallback):
            def __init__(self, client):
                self.client = client

            def connected(self, connection_id, endpoint, connected):
                pass

            def closed(self, connection_id, endpoint, caused_by_error):
                with self.client.file_gate_lock:
                    del self.client.file_gate_dict[endpoint]

        client.set_connection_callback(FielGateConnectCallbackInternal(self))
        if client.connect():
            client_info = RTMServerClient.FileGateInfo(client)
            with self.file_gate_lock:
                self.file_gate_dict[endpoint] = client_info
        return client_info

    def get_send_file_quest(self, send_file_info):
        sign = hashlib.md5((hashlib.md5(send_file_info.file_content).hexdigest().lower() + ':' + send_file_info.token).encode('utf-8')).hexdigest().lower()
        quest = Quest(send_file_info.send_type, params = {
            'pid' : self.pid,
            'token' : send_file_info.token,
            'mtype' : send_file_info.mtype,
            'from' : send_file_info.from_uid,
            'mid' : self.gen_mid(),
            'file' : send_file_info.file_content
        })
        if send_file_info.send_type == 'sendfile':
            quest.param('to', send_file_info.to_id)
        if send_file_info.send_type == 'sendfiles':
            quest.param('tos', send_file_info.to_ids)
        if send_file_info.send_type == 'sendroomfile':
            quest.param('rid', send_file_info.to_id)
        if send_file_info.send_type == 'sendgroupfile':
            quest.param('gid', send_file_info.to_id)
        attrs = '{"rtm":{"sign":"' + sign + '"'
        ext = ''
        idx = send_file_info.file_path.rfind('.')
        if idx >= 0:
            ext = send_file_info.file_path[idx + 1:]
        if len(ext) > 0:
            attrs += ', "ext":"' + ext + '"'
        attrs += '}}'
        quest.param('attrs', attrs)
        return quest
    
    def real_send_file_sync(self, send_type, from_uid, mtype, file_path, to_id = None, to_ids = None, timeout = 0):
        content = ''
        with open(file_path, 'rb') as f:
            content = f.read()
        if len(content) == 0:
            raise Exception('read file error')

        send_file_info = RTMServerClient.SendFileInfo(timeout)
        send_file_info.send_type = send_type
        send_file_info.from_uid = from_uid
        send_file_info.mtype = mtype
        send_file_info.file_path = file_path
        send_file_info.file_content = content
        send_file_info.to_id = to_id
        send_file_info.to_ids = to_ids

        mts = time.time() * 1000
        send_file_info.token, endpoint, error_code = self.file_token(from_uid, send_type, to_uids = to_ids, to_uid = to_id, rid = to_id, gid = to_id, timeout = send_file_info.remain_timeout)
        
        if error_code != FPNN_ERROR.FPNN_EC_OK:
            return None, error_code

        send_file_info.remain_timeout -= (time.time() * 1000 - mts)
        if send_file_info.remain_timeout <= 0:
            return None, FPNN_ERROR.FPNN_EC_CORE_TIMEOUT

        mts = time.time() * 1000
        file_gate_client_info = self.fetch_file_client(endpoint, send_file_info)
        file_gate_client = file_gate_client_info.client

        send_file_info.remain_timeout -= (time.time() * 1000 - mts)
        if send_file_info.remain_timeout <= 0:
            return None, FPNN_ERROR.FPNN_EC_CORE_TIMEOUT

        quest = self.get_send_file_quest(send_file_info)

        callback_internal = SendFileCallbackInternal(None)
        answer = file_gate_client.send_quest(quest, None, send_file_info.remain_timeout)
        file_gate_client_info.update_time = time.time()
        return callback_internal.get_result(answer)

    def real_send_file_async(self, send_type, from_uid, mtype, file_path, to_id = None, to_ids = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendFileCallback):
            raise Exception('callback type error')
        content = ''
        with open(file_path, 'rb') as f:
            content = f.read()
        if len(content) == 0:
            raise Exception('read file error')

        send_file_info = RTMServerClient.SendFileInfo(timeout)
        mts = time.time() * 1000
        send_file_info.send_type = send_type
        send_file_info.from_uid = from_uid
        send_file_info.mtype = mtype
        send_file_info.file_path = file_path
        send_file_info.file_content = content
        send_file_info.to_id = to_id
        send_file_info.to_ids = to_ids

        class MyFileTokenCallback(FileTokenCallback):
            def __init__(self, client, callback, send_file_info, mts):
                self.client = client
                self.send_callback = callback
                self.send_file_info = send_file_info
                self.mts = mts

            def callback(self, token, endpoint, error_code):
                if error_code == FPNN_ERROR.FPNN_EC_OK:
                    self.send_file_info.remain_timeout -= (time.time() * 1000 - self.mts)
                    if self.send_file_info.remain_timeout <= 0:
                        self.send_callback.callback(None, FPNN_ERROR.FPNN_EC_CORE_TIMEOUT)
                        return
                    self.mts = time.time() * 1000
                    file_gate_client_info = self.client.fetch_file_client(endpoint, self.send_file_info)
                    file_gate_client = file_gate_client_info.client

                    self.send_file_info.remain_timeout -= (time.time() * 1000 - self.mts)
                    if self.send_file_info.remain_timeout <= 0:
                        self.send_callback.callback(None, FPNN_ERROR.FPNN_EC_CORE_TIMEOUT)
                        return

                    send_file_info.token = token
                    quest = self.client.get_send_file_quest(self.send_file_info)
                    callback_internal = SendFileCallbackInternal(self.send_callback)
                    file_gate_client.send_quest(quest, callback_internal, self.send_file_info.remain_timeout)
                    file_gate_client_info.update_time = time.time()
                else:
                    self.send_callback.callback(None, error_code)

        self.file_token(from_uid, send_type, to_uids = to_ids, to_uid = to_id, rid = to_id, gid = to_id,callback = MyFileTokenCallback(self, callback, send_file_info, mts), timeout = send_file_info.remain_timeout)

    def send_file(self, from_uid, to_uid, mtype, file_path, callback = None, timeout = 0):
        if callback == None:
            return self.real_send_file_sync('sendfile', from_uid, mtype, file_path, to_id = to_uid, timeout = timeout)
        else:
            self.real_send_file_async('sendfile', from_uid, mtype, file_path, to_id = to_uid, callback = callback, timeout = timeout)

    def send_files(self, from_uid, to_uids, mtype, file_path, callback = None, timeout = 0):
        if callback == None:
            return self.real_send_file_sync('sendfiles', from_uid, mtype, file_path, to_ids = to_uids, timeout = timeout)
        else:
            self.real_send_file_async('sendfiles', from_uid, mtype, file_path, to_ids = to_uids, callback = callback, timeout = timeout)

    def send_room_file(self, from_uid, rid, mtype, file_path, callback = None, timeout = 0):
        if callback == None:
            return self.real_send_file_sync('sendroomfile', from_uid, mtype, file_path, to_id = rid, timeout = timeout)
        else:
            self.real_send_file_async('sendroomfile', from_uid, mtype, file_path, to_id = rid, callback = callback, timeout = timeout)

    def broadcast_file(self, from_uid, mtype, file_path, callback = None, timeout = 0):
        if callback == None:
            return self.real_send_file_sync('broadcastfile', from_uid, mtype, file_path, timeout = timeout)
        else:
            self.real_send_file_async('broadcastfile', from_uid, mtype, file_path, callback = callback, timeout = timeout)
    
    def send_group_file(self, from_uid, gid, mtype, file_path, callback = None, timeout = 0):
        if callback == None:
            return self.real_send_file_sync('sendgroupfile', from_uid, mtype, file_path, to_id = gid, timeout = timeout)
        else:
            self.real_send_file_async('sendgroupfile', from_uid, mtype, file_path, to_id = gid, callback = callback, timeout = timeout)

    def get_online_users(self, uids, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetOnlineUsersCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getonlineusers', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getonlineusers', ts),
            'salt' : salt,
            'ts' : ts,
            'uids' : uids
        })
        callback_internal = GetOnlineUsersCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def add_project_black(self, uid, btime, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('addprojectblack', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'addprojectblack', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'btime' : btime
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def remove_project_black(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('removeprojectblack', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'removeprojectblack', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def is_project_black(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, IsProjectBlackCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('isprojectblack', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'isprojectblack', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        callback_internal = IsProjectBlackCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def set_user_info(self, uid, oinfo = None, pinfo = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        if oinfo == None and pinfo == None:
            raise Exception('oinfo and pinfo must exist one')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('setuserinfo', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'setuserinfo', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        if oinfo != None:
            quest.param('oinfo', oinfo)
        if pinfo != None:
            quest.param('pinfo', pinfo)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_user_info(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetUserInfoCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getuserinfo', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getuserinfo', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        callback_internal = GetUserInfoCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_user_open_info(self, uids, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetUserOpenInfoCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getuseropeninfo', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getuseropeninfo', ts),
            'salt' : salt,
            'ts' : ts,
            'uids' : uids
        })
        callback_internal = GetUserOpenInfoCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)
        
    def add_friends(self, uid, friends, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('addfriends', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'addfriends', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'friends' : friends
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def delete_friends(self, uid, friends, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('delfriends', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'delfriends', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'friends' : friends
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_friends(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetFriendsCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getfriends', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getfriends', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        callback_internal = GetFriendsCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def is_friend(self, uid, fuid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, IsFriendCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('isfriend', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'isfriend', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'fuid' : fuid
        })
        callback_internal = IsFriendCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def is_friends(self, uid, fuids, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, IsFriendsCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('isfriends', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'isfriends', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'fuids' : fuids
        })
        callback_internal = IsFriendsCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def add_blacks(self, uid, blacks, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('addblacks', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'addblacks', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'blacks' : blacks
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def delete_blacks(self, uid, blacks, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('delblacks', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'delblacks', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'blacks' : blacks
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_blacks(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetBlacksCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getblacks', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getblacks', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        callback_internal = GetBlacksCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def is_black(self, uid, buid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, IsBlackCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('isblack', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'isblack', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'buid' : buid
        })
        callback_internal = IsBlackCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def is_blacks(self, uid, buids, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, IsBlacksCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('isblacks', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'isblacks', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'buids' : buids
        })
        callback_internal = IsBlacksCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def add_group_members(self, gid, uids, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('addgroupmembers', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'addgroupmembers', ts),
            'salt' : salt,
            'ts' : ts,
            'gid' : gid,
            'uids' : uids
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def delete_group_members(self, gid, uids, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('delgroupmembers', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'delgroupmembers', ts),
            'salt' : salt,
            'ts' : ts,
            'gid' : gid,
            'uids' : uids
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def delete_group(self, gid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('delgroup', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'delgroup', ts),
            'salt' : salt,
            'ts' : ts,
            'gid' : gid
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_group_members(self, gid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetGroupMembersCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getgroupmembers', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getgroupmembers', ts),
            'salt' : salt,
            'ts' : ts,
            'gid' : gid
        })
        callback_internal = GetGroupMembersCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def is_group_member(self, gid, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, IsGroupMemberCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('isgroupmember', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'isgroupmember', ts),
            'salt' : salt,
            'ts' : ts,
            'gid' : gid,
            'uid' : uid
        })
        callback_internal = IsGroupMemberCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_user_groups(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetUserGroupsCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getusergroups', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getusergroups', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        callback_internal = GetUserGroupsCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)
        
    def add_group_ban(self, gid, uid, btime, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('addgroupban', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'addgroupban', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'btime' : btime
        })
        if gid != None:
            quest.param('gid', gid)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def remove_group_ban(self, gid, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('removegroupban', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'removegroupban', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        if gid != None:
            quest.param('gid', gid)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)
        
    def is_ban_of_group(self, gid, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, IsBanOfGroupCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('isbanofgroup', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'isbanofgroup', ts),
            'salt' : salt,
            'ts' : ts,
            'gid' : gid,
            'uid' : uid
        })
        callback_internal = IsGroupMemberCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)
        
    def set_group_info(self, gid, oinfo = None, pinfo = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        if oinfo == None and pinfo == None:
            raise Exception('oinfo and pinfo must exist one')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('setgroupinfo', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'setgroupinfo', ts),
            'salt' : salt,
            'ts' : ts,
            'gid' : gid
        })
        if oinfo != None:
            quest.param('oinfo', oinfo)
        if pinfo != None:
            quest.param('pinfo', pinfo)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_group_info(self, gid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetGroupInfoCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getgroupinfo', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getgroupinfo', ts),
            'salt' : salt,
            'ts' : ts,
            'gid' : gid
        })
        callback_internal = GetGroupInfoCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def add_room_ban(self, rid, uid, btime, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('addroomban', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'addroomban', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'btime' : btime
        })
        if rid != None:
            quest.param('rid', rid)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def remove_room_ban(self, rid, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('removeroomban', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'removeroomban', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid
        })
        if rid != None:
            quest.param('rid', rid)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)
        
    def is_ban_of_room(self, rid, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, IsBanOfRoomCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('isbanofroom', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'isbanofroom', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : rid,
            'uid' : uid
        })
        callback_internal = IsBanOfRoomCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)


    def add_room_member(self, rid, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('addroommember', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'addroommember', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : rid,
            'uid' : uid
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def delete_room_member(self, rid, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('delroommember', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'delroommember', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : rid,
            'uid' : uid
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_room_members(self, rid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetRoomMembersCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getroommembers', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getroommembers', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : rid
        })
        callback_internal = GetRoomMembersCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_room_count(self, rids, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetRoomCountCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getroomcount', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getroomcount', ts),
            'salt' : salt,
            'ts' : ts,
            'rids' : rids
        })
        callback_internal = GetRoomCountCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def set_room_info(self, rid, oinfo = None, pinfo = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        if oinfo == None and pinfo == None:
            raise Exception('oinfo and pinfo must exist one')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('setroominfo', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'setroominfo', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : rid
        })
        if oinfo != None:
            quest.param('oinfo', oinfo)
        if pinfo != None:
            quest.param('pinfo', pinfo)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_room_info(self, rid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetRoomInfoCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getroominfo', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getroominfo', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : rid
        })
        callback_internal = GetRoomInfoCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def add_listen(self, gids = None, rids = None, uids = None, events = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        if gids == None and rids == None and uids == None and events == None:
            raise Exception('gids rids uids events must exist one')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('addlisten', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'addlisten', ts),
            'salt' : salt,
            'ts' : ts
        })

        listen_status = copy.deepcopy(self.listen_status_info)
        if gids != None:
            quest.param('gids', gids)
            listen_status.group_ids.update(gids)
        if rids != None:
            quest.param('rids', rids)
            listen_status.room_ids.update(rids)
        if uids != None:
            quest.param('uids', uids)
            listen_status.user_ids.update(uids)
        if events != None:
            quest.param('events', events)
            listen_status.events.update(events)

        callback_internal = ListenCallbackInternal(callback, self, listen_status)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def remove_listen(self, gids = None, rids = None, uids = None, events = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        if gids == None and rids == None and uids == None and events == None:
            raise Exception('gids rids uids events must exist one')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('removelisten', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'removelisten', ts),
            'salt' : salt,
            'ts' : ts
        })

        listen_status = copy.deepcopy(self.listen_status_info)
        if gids != None:
            quest.param('gids', gids)
            listen_status.group_ids.difference_update(gids)
        if rids != None:
            quest.param('rids', rids)
            listen_status.room_ids.difference_update(rids)
        if uids != None:
            quest.param('uids', uids)
            listen_status.user_ids.difference_update(uids)
        if events != None:
            quest.param('events', events)
            listen_status.events.difference_update(events)

        callback_internal = ListenCallbackInternal(callback, self, listen_status)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def set_listen(self, gids = None, rids = None, uids = None, events = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        if gids == None and rids == None and uids == None and events == None:
            raise Exception('gids rids uids events must exist one')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('setlisten', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'setlisten', ts),
            'salt' : salt,
            'ts' : ts
        })

        listen_status = copy.deepcopy(self.listen_status_info)
        if gids != None:
            quest.param('gids', gids)
            listen_status.group_ids = gids
        if rids != None:
            quest.param('rids', rids)
            listen_status.room_ids = rids
        if uids != None:
            quest.param('uids', uids)
            listen_status.user_ids = uids
        if events != None:
            quest.param('events', events)
            listen_status.events = events

        callback_internal = ListenCallbackInternal(callback, self, listen_status)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def set_all_listen(self, p2p = None, group = None, room = None, ev = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        if p2p == None and group == None and room == None and ev == None:
            raise Exception('gids rids uids events must exist one')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('setlisten', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'setlisten', ts),
            'salt' : salt,
            'ts' : ts
        })

        listen_status = copy.deepcopy(self.listen_status_info)
        if p2p != None:
            quest.param('p2p', p2p)
            listen_status.all_p2p = p2p
        if group != None:
            quest.param('group', group)
            listen_status.all_groups = group
        if room != None:
            quest.param('room', room)
            listen_status.all_rooms = room
        if ev != None:
            quest.param('ev', ev)
            listen_status.all_events = ev

        callback_internal = ListenCallbackInternal(callback, self, listen_status)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)
    
    def data_set(self, uid, key, value, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('dataset', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'dataset', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'key' : key,
            'val' : value
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def data_get(self, uid, key, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, DataGetCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('dataget', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'dataget', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'key' : key
        })
        callback_internal = DataGetCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def data_delete(self, uid, key, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('datadel', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'datadel', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'key' : key
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_message_num(self, message_type, xid, mtypes = None, begin = None, end = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetMessageNumCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getmsgnum', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getmsgnum', ts),
            'salt' : salt,
            'ts' : ts,
            'type' : message_type,
            'xid' : xid
        })
        if mtypes != None:
            quest.param('mtypes', mtypes)
        if begin != None:
            quest.param('begin', begin)
        if end != None:
            quest.param('end', end)

        callback_internal = GetMessageNumCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def invite_user_into_rtc_room(self, room_id, to_uids, from_uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('inviteUserIntoRTCRoom', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'inviteUserIntoRTCRoom', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : room_id,
            'toUids' : to_uids,
            'fromUid' : from_uid
        })

        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def close_rtc_room(self, room_id, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('call back type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('closeRTCRoom', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'closeRTCRoom', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : room_id
        })

        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def kick_out_from_rtc_room(self, uid, room_id, from_uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('call back type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('kickoutFromRTCRoom', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'kickoutFromRTCRoom', ts),
            'salt' : salt,
            'ts' : ts,
            'uid' : uid,
            'rid' : room_id,
            'fromUid' : from_uid
        })

        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_rtc_room_list(self, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetRTCRoomListCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getRTCRoomList', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getRTCRoomList', ts),
            'salt' : salt,
            'ts' : ts
        })

        callback_internal = GetRTCRoomListCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_rtc_room_members(self, room_id, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetRTCRoomMembersCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getRTCRoomMembers', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getRTCRoomMembers', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : room_id
        })

        callback_internal = GetRTCRoomMembersCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def get_rtc_room_member_count(self, room_id, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, GetRTCRoomMemberCountCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('getRTCRoomMemberCount', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'getRTCRoomMemberCount', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : room_id
        })

        callback_internal = GetRTCRoomMemberCountCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def set_rtc_room_mic_status(self, room_id, status, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('call back type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('setRTCRoomMicStatus', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'setRTCRoomMicStatus', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : room_id,
            'status' : status
        })

        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def pull_into_rtc_room(self, room_id, to_uids, type, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('call back type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('pullIntoRTCRoom', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'pullIntoRTCRoom', ts),
            'salt' : salt,
            'ts' : ts,
            'rid' : room_id,
            'toUids' : to_uids,
            'type' : type
        })

        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)

    def admin_command(self, room_id, uids, command, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('call back type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('adminCommand', params={
            'pid': self.pid,
            'sign': self.gen_sign(salt, 'adminCommand', ts),
            'salt': salt,
            'ts': ts,
            'rid': room_id,
            'uids': uids,
            'command': command
        })

        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)
        
    def clear_user_message(self, uid, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, BasicCallback):
            raise Exception('call back type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('clearusermsg', params={
            'pid': self.pid,
            'sign': self.gen_sign(salt, 'adminCommand', ts),
            'salt': salt,
            'ts': ts,
            'uid': uid
        })

        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout * 1000)
        else:
            answer = self.client.send_quest(quest, None, timeout * 1000)
            return callback_internal.get_result(answer)