#encoding=utf8

import sys
sys.path.append("..")
import threading
import hashlib
import time
from enum import Enum
from fpnn import *

class RTMServerPushMonitor(object):
    def __init__(self):
        pass

    def ping(self):
        pass

    def push_message(self, message):
        pass

    def push_group_message(self, message):
        pass

    def push_room_message(self, message):
        pass

    def push_event(self, pid, event, uid, time, endpoint, data):
        pass

    def push_file(self, message):
        pass

    def push_group_file(self, message):
        pass

    def push_room_file(self, message):
        pass

    def push_chat(self, message):
        pass

    def push_group_chat(self, message):
        pass

    def push_room_chat(self, message):
        pass

    def push_cmd(self, message):
        pass

    def push_group_cmd(self, message):
        pass

    def push_room_cmd(self, message):
        pass


