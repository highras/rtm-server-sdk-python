#encoding=utf8
from enum import Enum
import json

class ChatMessageType(Enum):
    TEXT = 30
    AUDIO = 31
    CMD = 32

class MessageType(Enum):
    P2P_MESSAGE = 1
    GROUP_MESSAGE = 2
    ROOM_MESSAGE = 3
    BROADCAST_MESSAGE = 4

class AudioInfo(object):
    def __init__(self):
        self.source_language = ""
        self.recognized_language = ""
        self.recognized_text = ""
        self.duration = 0

class TranslatedInfo(object):
    def __init__(self):
        self.source_language = ""
        self.target_language = ""
        self.source_text = ""
        self.target_text = ""

class RetrievedMessage(object):
    def __init__(self):
        self.cursor_id = 0
        self.message_type = 0
        self.message = None
        self.attrs = None
        self.modified_time = 0

class RTMMessage(object):
    def __init__(self):
        self.from_uid = 0
        self.to_id = 0
        self.message_type = 0
        self.message_id = 0
        self.message = None
        self.attrs = None
        self.modified_time = 0
        self.audio_info = None

class HistoryMessage(RTMMessage):
    def __init__(self):
        self.cursor_id = 0

class HistoryMessageResult(object):
    def __init__(self):
        self.count = 0
        self.last_cursor_id = 0
        self.begin_msec = 0
        self.end_msec = 0
        self.messages = []

class RegressiveStrategy(object):
    connect_failed_max_interval_milliseconds = 1500
    start_connect_failed_count = 5
    first_interval_seconds = 2
    max_interval_seconds = 120
    linear_regressive_count = 5

class ListenStatusInfo(object):
    def __init__(self):
        self.all_p2p = False
        self.all_groups = False
        self.all_rooms = False
        self.all_events = False
        self.user_ids = set()
        self.group_ids = set()
        self.room_ids = set()
        self.events = set()

def build_audio_info(msg):
    json_data = json.loads(msg)
    audio_info = AudioInfo()
    audio_info.source_language = json_data.get("sl", "")
    audio_info.recognized_language = json_data.get("rl", "")
    audio_info.recognized_text = json_data.get("rt", "")
    audio_info.duration = json_data.get("du", 0)
    return audio_info
