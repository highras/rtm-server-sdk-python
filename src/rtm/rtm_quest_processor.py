#encoding=utf8

import sys
sys.path.append("..")
import threading
import hashlib
import time
from enum import Enum
from fpnn import *

class RTMQuestProcessor(object):
    def __init__(self):
        pass

    def ping(self):
        pass

    def push_message(self, from_uid, to_uid, mtype, mid, msg, attrs, mtime):
        pass

    def push_group_message(self, from_uid, gid, mtype, mid, msg, attrs, mtime):
        pass

    def push_room_message(self, from_uid, rid, mtype, mid, msg, attrs, mtime):
        pass

    def push_event(self, pid, event, uid, time, endpoint, data):
        pass

    def push_file(self, from_uid, to_uid, mtype, mid, msg, attrs, mtime):
        pass

    def push_group_file(self, from_uid, gid, mtype, mid, msg, attrs, mtime):
        pass

    def push_room_file(self, from_uid, rid, mtype, mid, msg, attrs, mtime):
        pass

    def push_chat(self, from_uid, to_uid, mid, msg, attrs, mtime):
        pass

    def push_group_chat(self, from_uid, gid, mid, msg, attrs, mtime):
        pass

    def push_room_chat(self, from_uid, rid, mid, msg, attrs, mtime):
        pass

    def push_audio(self, from_uid, to_uid, mid, msg, attrs, mtime):
        pass

    def push_group_audio(self, from_uid, gid, mid, msg, attrs, mtime):
        pass

    def push_room_audio(self, from_uid, rid, mid, msg, attrs, mtime):
        pass

    def push_cmd(self, from_uid, to_uid, mid, msg, attrs, mtime):
        pass

    def push_group_cmd(self, from_uid, gid, mid, msg, attrs, mtime):
        pass

    def push_room_cmd(self, from_uid, rid, mid, msg, attrs, mtime):
        pass


