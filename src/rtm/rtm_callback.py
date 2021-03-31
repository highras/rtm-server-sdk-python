#encoding=utf8
import sys
sys.path.append("..")


class RTMConnectionCallback(object):
    def connected(self, connection_id, endpoint, connected, is_reconnect):
        pass

    def closed(self, connection_id, endpoint, caused_by_error, is_reconnect):
        pass

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
        MessageBase.__init__(self)

class RoomMessage(MessageBase):
    def __init__(self):
        MessageBase.__init__(self)

class BroadcastMessage(MessageBase):
    def __init__(self):
        MessageBase.__init__(self)

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

class CheckResult(object):
    def __init__(self):
        self.result = 0
        self.tags = []

class TextCheckResult(CheckResult):
    def __init__(self):
        CheckResult.__init__(self)
        self.text = str()
        self.wlist = []

class TextCheckCallback(object):
    def callback(self, result, error):
        pass

class CheckCallback(object):
    def callback(self, result, error):
        pass

class SpeechToTextResult(object):
    def __init__(self):
        self.text = str()
        self.lang = str()

class SpeechToTextCallback(object):
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

class GetBlacksCallback(object):
    def callback(self, uids, error):
        pass

class IsBlackCallback(object):
    def callback(self, ok, error):
        pass

class IsBlacksCallback(object):
    def callback(self, fuids, error):
        pass

class GetGroupMembersCallback(object):
    def callback(self, uids, error):
        pass

class GetRoomMembersCallback(object):
    def callback(self, uids, error):
        pass

class GetRoomCountCallback(object):
    def callback(self, count, error):
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

class GetDevicePushOptionResult(object):
    def __init__(self):
        self.p2p = dict()
        self.group = dict()

class GetDevicePushOptionCallback(object):
    def callback(self, result, error):
        pass

class GetMessageNumResult(object):
    def __init__(self):
        self.sender = 0
        self.num = 0

class GetMessageNumCallback(object):
    def callback(self, result, error):
        pass

class GetVoiceRoomListResult(object):
    def __init__(self):
        self.room_ids = []

class GetVoiceRoomListCallback(object):
    def callback(self, result, error):
        pass

class GetVoiceRoomMembersResult(object):
    def __init__(self):
        self.uids = []
        self.managers = []

class GetVoiceRoomMembersCallback(object):
    def callback(self, result, error):
        pass

class GetVoiceRoomMemberCountResult(object):
    def __init__(self):
        self.count = 0

class GetVoiceRoomMemberCountCallback(object):
    def callback(self, result, error):
        pass