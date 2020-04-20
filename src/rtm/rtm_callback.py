#encoding=utf8
import sys
sys.path.append("..")
from fpnn import *

class QuestError(object):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return 'Quest Error {0} : {1}'.format(self.code, self.message)

class GetTokenCallback(object):
    def callback(self, token, error):
        pass

class BasicCallback(object):
    def callback(self, error):
        pass

class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass

class MessageBase(object):
    def __init__(self):
        self.id = 0
        self.from_uid = 0
        self.mtype = 0
        self.mid = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0
        
class GroupMessage(MessageBase):
    def __init__(self):
        pass

class RoomMessage(MessageBase):
    def __init__(self):
        pass

class BroadcastMessage(MessageBase):
    def __init__(self):
        pass

class P2PMessage(object):
    def __init__(self):
        self.id = 0
        self.direction = 0
        self.mtype = 0
        self.mid = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0

class GetMessageResult(object):
    def __init__(self):
        self.num = 0
        self.lastid = 0
        self.begin = 0
        self.end = 0
        self.msgs = []

class GetGroupMessageResult(GetMessageResult):
    def __init__(self):
        GetMessageResult.__init__(self)

class GetRoomMessageResult(GetMessageResult):
    def __init__(self):
        GetMessageResult.__init__(self)

class GetBroadcastMessageResult(GetMessageResult):
    def __init__(self):
        GetMessageResult.__init__(self)

class GetP2PMessageResult(GetMessageResult):
    def __init__(self):
        GetMessageResult.__init__(self)

class GetGroupMessageCallback(object):
    def callback(self, result, error):
        pass

class GetRoomMessageCallback(object):
    def callback(self, result, error):
        pass

class GetBroadcastMessageCallback(object):
    def callback(self, result, error):
        pass

class GetP2PMessageCallback(object):
    def callback(self, result, error):
        pass

class MessageInfoResult(object):
    def __init__(self):
        self.id = 0
        self.mtype = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0

class GetMessageInfoCallback(object):
    def callback(self, result, error):
        pass

class TranslateResult(object):
    def __init__(self):
        self.source = str()
        self.target = str()
        self.source_text = str()
        self.target_text = str()

class TranslateCallback(object):
    def callback(self, result, error):
        pass

class ProfanityResult(object):
    def __init__(self):
        self.text = str()
        self.classification = []

class ProfanityCallback(object):
    def callback(self, result, error):
        pass

class TranscribeResult(object):
    def __init__(self):
        self.text = str()
        self.lang = str()

class TranscribeCallback(object):
    def callback(self, result, error):
        pass

class FileTokenCallback(object):
    def callback(self, token, endpoint, error):
        pass

class SendFileCallback(object):
    def callback(self, mtime, error):
        pass

class GetOnlineUsersCallback(object):
    def callback(self, uids, error):
        pass

class IsProjectBlackCallback(object):
    def callback(self, ok, error):
        pass

class GetUserInfoCallback(object):
    def callback(self, oinfo, pinfo, error):
        pass

class GetUserOpenInfoCallback(object):
    def callback(self, info, error):
        pass

class GetFriendsCallback(object):
    def callback(self, uids, error):
        pass

class IsFriendCallback(object):
    def callback(self, ok, error):
        pass

class IsFriendsCallback(object):
    def callback(self, fuids, error):
        pass

class GetGroupMembersCallback(object):
    def callback(self, uids, error):
        pass

class IsGroupMemberCallback(object):
    def callback(self, ok, error):
        pass

class GetUserGroupsCallback(object):
    def callback(self, gids, error):
        pass

class IsBanOfGroupCallback(object):
    def callback(self, ok, error):
        pass

class GetGroupInfoCallback(object):
    def callback(self, oinfo, pinfo, error):
        pass

class IsBanOfRoomCallback(object):
    def callback(self, ok, error):
        pass

class GetRoomInfoCallback(object):
    def callback(self, oinfo, pinfo, error):
        pass

class DataGetCallback(object):
    def callback(self, value, error):
        pass