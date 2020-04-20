#encoding=utf8

import sys
sys.path.append("..")
import threading
import hashlib
import time
from enum import Enum
from fpnn import *
from .rtm_quest_processor import *

DUP_FILTER_CLEAN_INTERVAL_SECONDS = 300
DUP_FILTER_TRIGGER_CLEAN_COUNT = 1000

class ChatMessageType(Enum):
    TEXT = 30
    AUDIO = 31
    CMD = 32

class DupP2PMessageKey():
    def __init__(self, sender, receiver, mid):
        self.sender = sender
        self.receiver = receiver
        self.mid = mid

    def __hash__(self):
        return hash(str(self.sender) + ':' + str(self.receiver) + ':' + str(self.mid))

    def __eq__(self, other):
        return (self.sender, self.receiver, self.mid) == (other.sender, other.receiver, other.mid)

class DupGroupMessageKey():
    def __init__(self, sender, group, mid):
        self.sender = sender
        self.group = group
        self.mid = mid

    def __hash__(self):
        return hash(str(self.sender) + ':' + str(self.group) + ':' + str(self.mid))

    def __eq__(self, other):
        return (self.sender, self.group, self.mid) == (other.sender, other.group, other.mid)

class DupRoomMessageKey():
    def __init__(self, sender, room, mid):
        self.sender = sender
        self.room = room
        self.mid = mid

    def __hash__(self):
        return hash(str(self.sender) + ':' + str(self.room) + ':' + str(self.mid))

    def __eq__(self, other):
        return (self.sender, self.room, self.mid) == (other.sender, other.room, other.mid)

class DupMessageFilter(object):
    def __init__(self):
        self.p2p_filter = {}
        self.group_filter = {}
        self.room_filter = {}

    def is_dup(self, mtype, key):
        filter_cache = None
        if mtype == 'p2p':
            filter_cache = self.p2p_filter
        elif mtype == 'group':
            filter_cache = self.group_filter
        else:
            filter_cache = self.room_filter
        now = int(time.time())
        is_dup = False
        ts = filter_cache.get(key, None)
        if ts == None:
            filter_cache[key] = now
            is_dup = False
        else:
            is_dup = True

        if len(filter_cache) > DUP_FILTER_TRIGGER_CLEAN_COUNT:
            threshold = now - DUP_FILTER_CLEAN_INTERVAL_SECONDS
            delete_keys = []
            for (key, value) in filter_cache.items():
                if value <= threshold:
                    delete_keys.append(key)
            for key in delete_keys:
                del filter_cache[key]
        return is_dup

class RtmQuestProcessorInternal(QuestProcessor):
    def __init__(self):
        self.processor = None
        self.dup_filter = DupMessageFilter() 

    def set_processor(self, processor):
        self.processor = processor

    def ping(self, connection, quest):
        connection.send_answer(Answer())
        self.processor.ping()

    def pushevent(self, connection, quest):
        connection.send_answer(Answer())
        pid = quest.get('pid', None)
        uid = quest.get('uid', None)
        event = quest.get('event', None)
        endpoint = quest.get('endpoint', None)
        time = quest.get('time', None)
        data = quest.get('data', None)
        try:
            self.processor.push_event(pid, event, uid, time, endpoint, data)
        except:
            pass

    def pushmsg(self, connection, quest):
        connection.send_answer(Answer())
        from_uid = quest.get('from', None)
        to_uid = quest.get('to', None)
        mtype = quest.get('mtype', None)
        mid = quest.get('mid', None)
        msg = quest.get('msg', None)
        attrs = quest.get('attrs', None)
        mtime = quest.get('mtime', None)
        if not self.dup_filter.is_dup('p2p', DupP2PMessageKey(from_uid, to_uid, mid)):
            try:
                if mtype == ChatMessageType.TEXT.value:
                    self.processor.push_chat(from_uid, to_uid, mid, msg, attrs, mtime)
                elif mtype == ChatMessageType.AUDIO.value:
                    self.processor.push_audio(from_uid, to_uid, mid, msg, attrs, mtime)
                elif mtype == ChatMessageType.CMD.value:
                    self.processor.push_cmd(from_uid, to_uid, mid, msg, attrs, mtime)
                else:
                    self.processor.push_message(from_uid, to_uid, mtype, mid, msg, attrs, mtime)
            except:
                pass

    def pushgroupmsg(self, connection, quest):
        connection.send_answer(Answer())
        from_uid = quest.get('from', None)
        gid = quest.get('gid', None)
        mtype = quest.get('mtype', None)
        mid = quest.get('mid', None)
        msg = quest.get('msg', None)
        attrs = quest.get('attrs', None)
        mtime = quest.get('mtime', None)
        if not self.dup_filter.is_dup('group', DupGroupMessageKey(from_uid, gid, mid)):
            try:
                if mtype == ChatMessageType.TEXT.value:
                    self.processor.push_group_chat(from_uid, gid, mid, msg, attrs, mtime)
                elif mtype == ChatMessageType.AUDIO.value:
                    self.processor.push_group_audio(from_uid, gid, mid, msg, attrs, mtime)
                elif mtype == ChatMessageType.CMD.value:
                    self.processor.push_group_cmd(from_uid, gid, mid, msg, attrs, mtime)
                else:
                    self.processor.push_group_message(from_uid, gid, mtype, mid, msg, attrs, mtime)
            except:
                pass

    def pushroommsg(self, connection, quest):
        connection.send_answer(Answer())
        from_uid = quest.get('from', None)
        rid = quest.get('rid', None)
        mtype = quest.get('mtype', None)
        mid = quest.get('mid', None)
        msg = quest.get('msg', None)
        attrs = quest.get('attrs', None)
        mtime = quest.get('mtime', None)
        if not self.dup_filter.is_dup('room', DupRoomMessageKey(from_uid, rid, mid)):
            try:
                if mtype == ChatMessageType.TEXT.value:
                    self.processor.push_room_chat(from_uid, rid, mid, msg, attrs, mtime)
                elif mtype == ChatMessageType.AUDIO.value:
                    self.processor.push_room_audio(from_uid, rid, mid, msg, attrs, mtime)
                elif mtype == ChatMessageType.CMD.value:
                    self.processor.push_room_cmd(from_uid, rid, mid, msg, attrs, mtime)
                else:
                    self.processor.push_room_message(from_uid, rid, mtype, mid, msg, attrs, mtime)
            except:
                pass
    
    def pushfile(self, connection, quest):
        connection.send_answer(Answer())
        from_uid = quest.get('from', None)
        to_uid = quest.get('to', None)
        mtype = quest.get('mtype', None)
        mid = quest.get('mid', None)
        msg = quest.get('msg', None)
        attrs = quest.get('attrs', None)
        mtime = quest.get('mtime', None)
        if not self.dup_filter.is_dup('p2p', DupP2PMessageKey(from_uid, to_uid, mid)):
            try:
                self.processor.push_file(from_uid, to_uid, mtype, mid, msg, attrs, mtime)
            except:
                pass 

    def pushgroupfile(self, connection, quest):
        connection.send_answer(Answer())
        from_uid = quest.get('from', None)
        gid = quest.get('gid', None)
        mtype = quest.get('mtype', None)
        mid = quest.get('mid', None)
        msg = quest.get('msg', None)
        attrs = quest.get('attrs', None)
        mtime = quest.get('mtime', None)
        if not self.dup_filter.is_dup('group', DupGroupMessageKey(from_uid, gid, mid)):
            try:
                self.processor.push_group_file(from_uid, gid, mtype, mid, msg, attrs, mtime)
            except:
                pass

    def pushroomfile(self, connection, quest):
        connection.send_answer(Answer())
        from_uid = quest.get('from', None)
        rid = quest.get('rid', None)
        mtype = quest.get('mtype', None)
        mid = quest.get('mid', None)
        msg = quest.get('msg', None)
        attrs = quest.get('attrs', None)
        mtime = quest.get('mtime', None)
        if not self.dup_filter.is_dup('room', DupRoomMessageKey(from_uid, rid, mid)):
            try:
                self.processor.push_room_file(from_uid, rid, mtype, mid, msg, attrs, mtime)
            except:
                pass