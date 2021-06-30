#encoding=utf8
from enum import Enum
import json

class ChatMessageType(Enum):
    TEXT = 30
    CMD = 32

class MessageType(Enum):
    P2P_MESSAGE = 1
    GROUP_MESSAGE = 2
    ROOM_MESSAGE = 3
    BROADCAST_MESSAGE = 4

class FileInfo(object):
    def __init__(self):
        self.url = ""
        self.size = 0
        self.surl = ""
        self.is_rtm_audio = False
        self.language = ""
        self.duration = 0
    @staticmethod
    def parse_file_message(message):
        try:
            info_dict = json.loads(message.message)
            message.file_info.url = info_dict.get('url', '')
            message.file_info.size = info_dict.get('size', 0)
            message.file_info.surl = info_dict.get('surl', '')
            message.message = None
        except:
            pass
        return message

    @staticmethod
    def parse_file_attrs(message):
        try:
            attrs_dict = json.loads(message.attrs)
            rtmAttrsDict = attrs_dict['rtm']
            file_type = rtmAttrsDict.get('type', None)
            if file_type != None and file_type == 'audiomsg':
                message.file_info.is_rtm_audio = True
            if message.file_info.is_rtm_audio:
                message.file_info.language = rtmAttrsDict.get('lang', '')
                message.file_info.duration = rtmAttrsDict.get('duration', 0)

            user_attrs_dict = attrs_dict['custom']
            try:
                message.attrs = json.dumps(user_attrs_dict)
            except:
                try:
                    message.attrs = str(user_attrs_dict)
                except:
                    pass
        except:
            pass
        return message

    @staticmethod
    def build_file_info(message):
        message.file_info = FileInfo()
        message = FileInfo.parse_file_message(message)
        message = FileInfo.parse_file_attrs(message)
        return message

class RetrievedMessage(object):
    def __init__(self):
        self.cursor_id = 0
        self.message_type = 0
        self.message = None
        self.attrs = None
        self.modified_time = 0
        self.file_info = None

class RTMMessage(object):
    def __init__(self):
        self.from_uid = 0
        self.to_id = 0
        self.message_type = 0
        self.message_id = 0
        self.message = None
        self.attrs = None
        self.modified_time = 0
        self.file_info = None

class HistoryMessage(RTMMessage):
    def __init__(self):
        RTMMessage.__init__(self)
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

class AdministratorCommand(Enum):
    AppointAdministrator    = 0 #赋予管理员权限
    DismissAdministrator    = 1 #剥夺管理员权限
    ForbidSendingAudio      = 2 #禁止发送音频数据
    AllowSendingAudio       = 3 #允许发送视频数据
    ForbidSendingVideo      = 4 #禁止发送视频数据
    AllowSendingVideo       = 5 #允许发送视频数据
    CloseOthersMicroPhone   = 6 #关闭他人麦克风
    CloseOthersMicroCamera  = 7 #关闭他人摄像头
