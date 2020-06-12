#encoding=utf8

import sys
sys.path.append("..")
import threading
import hashlib
import time
from enum import Enum
from fpnn import *
from .rtm_callback import *
from .rtm_callback_internal import *
from .rtm_quest_processor_internal import *

RTM_SDK_VERSION = '2.1.0'
RTM_API_VERSION = '2.0.3'

class MessageType(Enum):
    P2P_MESSAGE = 1
    GROUP_MESSAGE = 2
    ROOM_MESSAGE = 3
    BROADCAST_MESSAGE = 4

class RTMServerClient(object):
    def __init__(self, pid, secret, endpoint, reconnect, timeout = 0):
        self.pid = pid
        self.secret = secret
        arr = endpoint.split(':')
        self.client = TCPClient(arr[0], int(arr[1]), reconnect)
        self.client.set_quest_timeout(timeout)
        self.seq_lock = threading.Lock()
        self.seq = 0
        self.processor = None

    def set_quest_timeout(self, timeout):
        self.client.set_quest_timeout(timeout)

    def set_connection_callback(self, callback):
        self.client.set_connection_callback(callback)

    def enable_encryptor_by_pem_file(self, pem_pub_file, curve_name = 'secp256k1', strength = 128):
        self.client.enable_encryptor_by_pem_file(pem_pub_file, curve_name, strength)

    def set_quest_processor(self, processor):
        if self.processor == None:
            self.processor = RtmQuestProcessorInternal()
        self.processor.set_processor(processor)
        self.client.set_quest_processor(self.processor)

    def close(self):
        self.client.close()

    def reconnect(self):
        self.client.reconnect()

    def destory(self):
        self.client.destory()

    def gen_mid(self):
        with self.seq_lock:
            self.seq += 1
            return (int(time.time()) << 32) | (self.seq & 0xffffff)

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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def kickout(self, uid, ce = None, callback = None, timeout = 0):
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
        if ce != None:
            quest.param('ce', ce)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def send_message(self, mtype, from_uid, to_uid, msg, attrs, mid = 0, callback = None, timeout = 0):
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
            'msg' : msg,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def send_messages(self, mtype, from_uid, to_uids, msg, attrs, mid = 0, callback = None, timeout = 0):
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
            'msg' : msg,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def send_group_message(self, mtype, from_uid, gid, msg, attrs, mid = 0, callback = None, timeout = 0):
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
            'msg' : msg,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def send_room_message(self, mtype, from_uid, rid, msg, attrs, mid = 0, callback = None, timeout = 0):
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
            'msg' : msg,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def broadcast_message(self, mtype, from_uid, msg, attrs, mid = 0, callback = None, timeout = 0):
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
            'msg' : msg,
            'attrs' : attrs
        })
        callback_internal = SendMessageCallbackInternal(callback, mid)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
        callback_internal = GetP2PMessageCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def get_p2p_message_info(self, mid, from_uid, to_uid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, to_uid, MessageType.P2P_MESSAGE.value, callback, timeout)

    def get_group_message_info(self, mid, from_uid, gid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, gid, MessageType.GROUP_MESSAGE.value, callback, timeout)

    def get_room_message_info(self, mid, from_uid, rid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, rid, MessageType.ROOM_MESSAGE.value, callback, timeout)

    def get_broadcast_message_info(self, mid, from_uid, callback = None, timeout = 0):
        return self.get_message_info(mid, from_uid, 0, MessageType.BROADCAST_MESSAGE.value, callback, timeout)

    def send_chat(self, from_uid, to_uid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_message(ChatMessageType.TEXT.value, from_uid, to_uid, msg, attrs, mid, callback, timeout)

    def send_chats(self, from_uid, to_uids, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_messages(ChatMessageType.TEXT.value, from_uid, to_uids, msg, attrs, mid, callback, timeout)

    def send_group_chat(self, from_uid, gid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_group_message(ChatMessageType.TEXT.value, from_uid, gid, msg, attrs, mid, callback, timeout)

    def send_room_chat(self, from_uid, rid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_room_message(ChatMessageType.TEXT.value, from_uid, rid, msg, attrs, mid, callback, timeout)

    def broadcast_chat(self, from_uid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.broadcast_message(ChatMessageType.TEXT.value, from_uid, msg, attrs, mid, callback, timeout)

    def send_audio(self, from_uid, to_uid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_message(ChatMessageType.AUDIO.value, from_uid, to_uid, msg, attrs, mid, callback, timeout)

    def send_audios(self, from_uid, to_uids, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_messages(ChatMessageType.AUDIO.value, from_uid, to_uids, msg, attrs, mid, callback, timeout)

    def send_group_audio(self, from_uid, gid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_group_message(ChatMessageType.AUDIO.value, from_uid, gid, msg, attrs, mid, callback, timeout)

    def send_room_audio(self, from_uid, rid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_room_message(ChatMessageType.AUDIO.value, from_uid, rid, msg, attrs, mid, callback, timeout)

    def broadcast_audio(self, from_uid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.broadcast_message(ChatMessageType.AUDIO.value, from_uid, msg, attrs, mid, callback, timeout)

    def send_cmd(self, from_uid, to_uid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_message(ChatMessageType.CMD.value, from_uid, to_uid, msg, attrs, mid, callback, timeout)

    def send_cmds(self, from_uid, to_uids, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_messages(ChatMessageType.CMD.value, from_uid, to_uids, msg, attrs, mid, callback, timeout)

    def send_group_cmd(self, from_uid, gid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_group_message(ChatMessageType.CMD.value, from_uid, gid, msg, attrs, mid, callback, timeout)

    def send_room_cmd(self, from_uid, rid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.send_room_message(ChatMessageType.CMD.value, from_uid, rid, msg, attrs, mid, callback, timeout)

    def broadcast_cmd(self, from_uid, msg, attrs, mid = 0, callback = None, timeout = 0):
        return self.broadcast_message(ChatMessageType.CMD.value, from_uid, msg, attrs, mid, callback, timeout)

    def get_group_chat(self, uid, gid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0):
        return self.get_group_message(uid, gid, desc, num, begin, end, lastid, [ChatMessageType.TEXT.value, ChatMessageType.AUDIO.value, ChatMessageType.CMD.value], callback, timeout)

    def get_room_chat(self, uid, rid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0):
        return self.get_room_message(uid, rid, desc, num, begin, end, lastid, [ChatMessageType.TEXT.value, ChatMessageType.AUDIO.value, ChatMessageType.CMD.value], callback, timeout)

    def get_broadcast_chat(self, uid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0):
        return self.get_broadcast_message(uid, desc, num, begin, end, lastid, [ChatMessageType.TEXT.value, ChatMessageType.AUDIO.value, ChatMessageType.CMD.value], callback, timeout)

    def get_p2p_chat(self, uid, ouid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0):
        return self.get_p2p_message(uid, ouid, desc, num, begin, end, lastid, [ChatMessageType.TEXT.value, ChatMessageType.AUDIO.value, ChatMessageType.CMD.value], callback, timeout)

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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def profanity(self, text, classify = False, uid = None, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, ProfanityCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('profanity', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'profanity', ts),
            'salt' : salt,
            'ts' : ts,
            'text' : text,
            'classify' : classify
        })
        if uid != None:
            quest.param('uid', uid)
        callback_internal = ProfanityCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def transcribe(self, audio, uid = None, profanity_filter = False, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, TranscribeCallback):
            raise Exception('callback type error')
        ts = int(time.time())
        salt = self.gen_mid()
        quest = Quest('transcribe', params = {
            'pid' : self.pid,
            'sign' : self.gen_sign(salt, 'transcribe', ts),
            'salt' : salt,
            'ts' : ts,
            'audio' : audio,
            'profanityFilter' : profanity_filter
        })
        if uid != None:
            quest.param('uid', uid)
        callback_internal = TranscribeCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def file_token(self, from_uid, cmd, to_uidss = None, to_uid = None, rid = None, gid = None, callback = None, timeout = 0):
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def send_file(self, from_uid, to_uid, mtype, file, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendFileCallback):
            raise Exception('callback type error')
        content = ''
        with open(file, 'rb') as f:
            content = f.read()
        if len(content) == 0:
            raise Exception('read file error')
        token, endpoint, error = self.file_token(from_uid, 'sendfile', to = to_uid, timeout = timeout)
        if error != None:
            if callback == None:
                return None, error
            else:
                callback.callback(None, error)
                return
        arr = endpoint.split(':')
        file_client = TCPClient(arr[0], int(arr[1]), True)
        file_client.set_quest_timeout(timeout)
        sign = hashlib.md5((hashlib.md5(content).hexdigest().lower() + ':' + token).encode('utf-8')).hexdigest().lower()
        quest = Quest('sendfile', params = {
            'pid' : self.pid,
            'token' : token,
            'mtype' : mtype,
            'from' : from_uid,
            'to' : to_uid,
            'mid' : self.gen_mid(),
            'file' : content
        })
        attrs = '{"sign":"' + sign + '"'
        file_arr = file.split('.')
        if len(file_arr) >= 2:
            attrs += ', "ext":"' + file_arr[len(file_arr) - 1] + '"'
        attrs += '}'
        quest.param('attrs', attrs)
        callback_internal = SendFileCallbackInternal(callback)
        if callback != None:
            file_client.send_quest(quest, callback_internal, timeout)
        else:
            answer = file_client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def send_files(self, from_uid, to_uids, mtype, file, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendFileCallback):
            raise Exception('callback type error')
        content = ''
        with open(file, 'rb') as f:
            content = f.read()
        if len(content) == 0:
            raise Exception('read file error')
        token, endpoint, error = self.file_token(from_uid, 'sendfiles', tos = to_uids, timeout = timeout)
        if error != None:
            if callback == None:
                return None, error
            else:
                callback.callback(None, error)
                return
        arr = endpoint.split(':')
        file_client = TCPClient(arr[0], int(arr[1]), True)
        file_client.set_quest_timeout(timeout)
        sign = hashlib.md5((hashlib.md5(content).hexdigest().lower() + ':' + token).encode('utf-8')).hexdigest().lower()
        quest = Quest('sendfiles', params = {
            'pid' : self.pid,
            'token' : token,
            'mtype' : mtype,
            'from' : from_uid,
            'tos' : to_uids,
            'mid' : self.gen_mid(),
            'file' : content
        })
        attrs = '{"sign":"' + sign + '"'
        file_arr = file.split('.')
        if len(file_arr) >= 2:
            attrs += ', "ext":"' + file_arr[len(file_arr) - 1] + '"'
        attrs += '}'
        quest.param('attrs', attrs)
        callback_internal = SendFileCallbackInternal(callback)
        if callback != None:
            file_client.send_quest(quest, callback_internal, timeout)
        else:
            answer = file_client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def send_room_file(self, from_uid, rid, mtype, file, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendFileCallback):
            raise Exception('callback type error')
        content = ''
        with open(file, 'rb') as f:
            content = f.read()
        if len(content) == 0:
            raise Exception('read file error')
        token, endpoint, error = self.file_token(from_uid, 'sendroomfile', rid = rid, timeout = timeout)
        if error != None:
            if callback == None:
                return None, error
            else:
                callback.callback(None, error)
                return
        arr = endpoint.split(':')
        file_client = TCPClient(arr[0], int(arr[1]), True)
        file_client.set_quest_timeout(timeout)
        sign = hashlib.md5((hashlib.md5(content).hexdigest().lower() + ':' + token).encode('utf-8')).hexdigest().lower()
        quest = Quest('sendroomfile', params = {
            'pid' : self.pid,
            'token' : token,
            'mtype' : mtype,
            'from' : from_uid,
            'rid' : rid,
            'mid' : self.gen_mid(),
            'file' : content
        })
        attrs = '{"sign":"' + sign + '"'
        file_arr = file.split('.')
        if len(file_arr) >= 2:
            attrs += ', "ext":"' + file_arr[len(file_arr) - 1] + '"'
        attrs += '}'
        quest.param('attrs', attrs)
        callback_internal = SendFileCallbackInternal(callback)
        if callback != None:
            file_client.send_quest(quest, callback_internal, timeout)
        else:
            answer = file_client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def broadcast_file(self, from_uid, mtype, file, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendFileCallback):
            raise Exception('callback type error')
        content = ''
        with open(file, 'rb') as f:
            content = f.read()
        if len(content) == 0:
            raise Exception('read file error')
        token, endpoint, error = self.file_token(from_uid, 'broadcastfile', timeout = timeout)
        if error != None:
            if callback == None:
                return None, error
            else:
                callback.callback(None, error)
                return
        arr = endpoint.split(':')
        file_client = TCPClient(arr[0], int(arr[1]), True)
        file_client.set_quest_timeout(timeout)
        sign = hashlib.md5((hashlib.md5(content).hexdigest().lower() + ':' + token).encode('utf-8')).hexdigest().lower()
        quest = Quest('broadcastfile', params = {
            'pid' : self.pid,
            'token' : token,
            'mtype' : mtype,
            'from' : from_uid,
            'mid' : self.gen_mid(),
            'file' : content
        })
        attrs = '{"sign":"' + sign + '"'
        file_arr = file.split('.')
        if len(file_arr) >= 2:
            attrs += ', "ext":"' + file_arr[len(file_arr) - 1] + '"'
        attrs += '}'
        quest.param('attrs', attrs)
        callback_internal = SendFileCallbackInternal(callback)
        if callback != None:
            file_client.send_quest(quest, callback_internal, timeout)
        else:
            answer = file_client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

    def send_group_file(self, from_uid, gid, mtype, file, callback = None, timeout = 0):
        if callback != None and not isinstance(callback, SendFileCallback):
            raise Exception('callback type error')
        content = ''
        with open(file, 'rb') as f:
            content = f.read()
        if len(content) == 0:
            raise Exception('read file error')
        token, endpoint, error = self.file_token(from_uid, 'sendgroupfile', gid = gid, timeout = timeout)
        if error != None:
            if callback == None:
                return None, error
            else:
                callback.callback(None, error)
                return
        arr = endpoint.split(':')
        file_client = TCPClient(arr[0], int(arr[1]), True)
        file_client.set_quest_timeout(timeout)
        sign = hashlib.md5((hashlib.md5(content).hexdigest().lower() + ':' + token).encode('utf-8')).hexdigest().lower()
        quest = Quest('sendgroupfile', params = {
            'pid' : self.pid,
            'token' : token,
            'mtype' : mtype,
            'from' : from_uid,
            'gid' : gid,
            'mid' : self.gen_mid(),
            'file' : content
        })
        attrs = '{"sign":"' + sign + '"'
        file_arr = file.split('.')
        if len(file_arr) >= 2:
            attrs += ', "ext":"' + file_arr[len(file_arr) - 1] + '"'
        attrs += '}'
        quest.param('attrs', attrs)
        callback_internal = SendFileCallbackInternal(callback)
        if callback != None:
            file_client.send_quest(quest, callback_internal, timeout)
        else:
            answer = file_client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)

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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            'gid' : gid,
            'uid' : uid,
            'btime' : btime
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            'gid' : gid,
            'uid' : uid
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            'rid' : rid,
            'uid' : uid,
            'btime' : btime
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            'rid' : rid,
            'uid' : uid
        })
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
        if gids != None:
            quest.param('gids', gids)
        if rids != None:
            quest.param('rids', rids)
        if uids != None:
            quest.param('uids', uids)
        if events != None:
            quest.param('events', events)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
        if gids != None:
            quest.param('gids', gids)
        if rids != None:
            quest.param('rids', rids)
        if uids != None:
            quest.param('uids', uids)
        if events != None:
            quest.param('events', events)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
        if gids != None:
            quest.param('gids', gids)
        if rids != None:
            quest.param('rids', rids)
        if uids != None:
            quest.param('uids', uids)
        if events != None:
            quest.param('events', events)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
        if p2p != None:
            quest.param('p2p', p2p)
        if group != None:
            quest.param('group', group)
        if room != None:
            quest.param('room', room)
        if ev != None:
            quest.param('ev', ev)
        callback_internal = BasicCallbackInternal(callback)
        if callback != None:
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
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
            self.client.send_quest(quest, callback_internal, timeout)
        else:
            answer = self.client.send_quest(quest, None, timeout)
            return callback_internal.get_result(answer)
