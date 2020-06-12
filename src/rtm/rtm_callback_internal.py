import sys
sys.path.append("..")
from fpnn import *
from .rtm_callback import *

class GetTokenCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            token = answer.get("token", None)
            if token == None:
                return None, QuestError(RTM_ERROR.RTM_EC_GET_ANSWER_PARAM_ERROR.value, "answer param error")
            else:
                return token, None

    def callback(self, answer):
        token, error = self.get_result(answer)
        self.real_callback.callback(token, error)

class BasicCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return QuestError(answer.error_code, answer.error_message)
        else:
            return None

    def callback(self, answer):
        error = self.get_result(answer)
        self.real_callback.callback(error)

class SendMessageCallbackInternal(QuestCallback):
    def __init__(self, real_callback, mid):
        self.real_callback = real_callback
        self.mid = mid

    def get_result(self, answer):
        if answer.is_error():
            return None, None, QuestError(answer.error_code, answer.error_message)
        else:
            mtime = answer.get("mtime", None)
            if mtime == None:
                return self.mid, None, QuestError(RTM_ERROR.RTM_EC_GET_ANSWER_PARAM_ERROR.value, "answer param error")
            else:
                return self.mid, mtime, None

    def callback(self, answer):
        mid, mtime, error = self.get_result(answer)
        self.real_callback.callback(mid, mtime, error)

class GetGroupMessageCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            result = GetGroupMessageResult()
            result.num = answer.get("num", 0)
            result.lastid = answer.get("lastid", 0)
            result.begin = answer.get("begin", 0)
            result.end = answer.get("end", 0)
            msgs = answer.get("msgs", [])
            for m in msgs:
                if len(m) != 8:
                    continue
                msg = GroupMessage()
                msg.id = m[0]
                msg.from_uid = m[1]
                msg.mtype = m[2]
                msg.mid = m[3]
                msg.msg = m[5]
                msg.attrs = m[6]
                msg.mtime = m[7]
                result.msgs.append(msg)
            return result, None

    def callback(self, answer):
        result, error = self.get_result(answer)
        self.real_callback.callback(result, error)

class GetRoomMessageCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            result = GetRoomMessageResult()
            result.num = answer.get("num", 0)
            result.lastid = answer.get("lastid", 0)
            result.begin = answer.get("begin", 0)
            result.end = answer.get("end", 0)
            msgs = answer.get("msgs", [])
            for m in msgs:
                if len(m) != 8:
                    continue
                msg = RoomMessage()
                msg.id = m[0]
                msg.from_uid = m[1]
                msg.mtype = m[2]
                msg.mid = m[3]
                msg.msg = m[5]
                msg.attrs = m[6]
                msg.mtime = m[7]
                result.msgs.append(msg)
            return result, None

    def callback(self, answer):
        result, error = self.get_result(answer)
        self.real_callback.callback(result, error)

class GetBroadcastMessageCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            result = GetBroadcastMessageResult()
            result.num = answer.get("num", 0)
            result.lastid = answer.get("lastid", 0)
            result.begin = answer.get("begin", 0)
            result.end = answer.get("end", 0)
            msgs = answer.get("msgs", [])
            for m in msgs:
                if len(m) != 8:
                    continue
                msg = BroadcastMessage()
                msg.id = m[0]
                msg.from_uid = m[1]
                msg.mtype = m[2]
                msg.mid = m[3]
                msg.msg = m[5]
                msg.attrs = m[6]
                msg.mtime = m[7]
                result.msgs.append(msg)
            return result, None

    def callback(self, answer):
        result, error = self.get_result(answer)
        self.real_callback.callback(result, error)

class GetP2PMessageCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            result = GetP2PMessageResult()
            result.num = answer.get("num", 0)
            result.lastid = answer.get("lastid", 0)
            result.begin = answer.get("begin", 0)
            result.end = answer.get("end", 0)
            msgs = answer.get("msgs", [])
            for m in msgs:
                if len(m) != 8:
                    continue
                msg = P2PMessage()
                msg.id = m[0]
                msg.direction = m[1]
                msg.mtype = m[2]
                msg.mid = m[3]
                msg.msg = m[5]
                msg.attrs = m[6]
                msg.mtime = m[7]
                result.msgs.append(msg)
            return result, None

    def callback(self, answer):
        result, error = self.get_result(answer)
        self.real_callback.callback(result, error)

class GetMessageInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            result = MessageInfoResult()
            result.id = answer.get("id", 0)
            result.mtype = answer.get("mtype", 0)
            result.msg = answer.get("msg", str())
            result.attrs = answer.get("attrs", str())
            result.mtime = answer.get("mtime", 0)
            return result, None

    def callback(self, answer):
        result, error = self.get_result(answer)
        self.real_callback.callback(result, error)

class TranslateCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            result = TranslateResult()
            result.source = answer.get("source", str())
            result.target = answer.get("target", str())
            result.source_text = answer.get("sourceText", str())
            result.target_text = answer.get("targetText", str())
            return result, None

    def callback(self, answer):
        result, error = self.get_result(answer)
        self.real_callback.callback(result, error)

class ProfanityCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            result = ProfanityResult()
            result.text = answer.get("text", str())
            result.classification = answer.get("classification", [])
            return result, None

    def callback(self, answer):
        result, error = self.get_result(answer)
        self.real_callback.callback(result, error)

class TranscribeCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            result = TranscribeResult()
            result.text = answer.get("text", str())
            result.lang = answer.get("lang", str())
            return result, None

    def callback(self, answer):
        result, error = self.get_result(answer)
        self.real_callback.callback(result, error)

class FileTokenCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, None, QuestError(answer.error_code, answer.error_message)
        else:
            token = answer.get("token", str())
            endpoint = answer.get("endpoint", str())
            return token, endpoint, None

    def callback(self, answer):
        token, endpoint, error = self.get_result(answer)
        self.real_callback.callback(token, endpoint, error)

class SendFileCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            mtime = answer.get("mtime", 0)
            return mtime, None

    def callback(self, answer):
        mtime, error = self.get_result(answer)
        self.real_callback.callback(mtime, error)

class GetOnlineUsersCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            uids = answer.get("uids", [])
            return uids, None

    def callback(self, answer):
        uids, error = self.get_result(answer)
        self.real_callback.callback(uids, error)

class IsProjectBlackCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            ok = answer.get("ok", False)
            return ok, None

    def callback(self, answer):
        ok, error = self.get_result(answer)
        self.real_callback.callback(ok, error)

class GetUserInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, None, QuestError(answer.error_code, answer.error_message)
        else:
            oinfo = answer.get("oinfo", None)
            pinfo = answer.get("pinfo", None)
            return oinfo, pinfo, None

    def callback(self, answer):
        oinfo, pinfo, error = self.get_result(answer)
        self.real_callback.callback(oinfo, pinfo, error)

class GetUserOpenInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            info = answer.get("info", {})
            return info, None

    def callback(self, answer):
        info, error = self.get_result(answer)
        self.real_callback.callback(info, error)

class GetFriendsCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            uids = answer.get("uids", [])
            return uids, None

    def callback(self, answer):
        uids, error = self.get_result(answer)
        self.real_callback.callback(uids, error)

class IsFriendCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            ok = answer.get("ok", False)
            return ok, None

    def callback(self, answer):
        ok, error = self.get_result(answer)
        self.real_callback.callback(ok, error)

class IsFriendsCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            fuids = answer.get("fuids", [])
            return fuids, None

    def callback(self, answer):
        fuids, error = self.get_result(answer)
        self.real_callback.callback(fuids, error)

class GetBlacksCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            uids = answer.get("uids", [])
            return uids, None

    def callback(self, answer):
        uids, error = self.get_result(answer)
        self.real_callback.callback(uids, error)

class IsBlackCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            ok = answer.get("ok", False)
            return ok, None

    def callback(self, answer):
        ok, error = self.get_result(answer)
        self.real_callback.callback(ok, error)

class IsBlacksCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            fuids = answer.get("buids", [])
            return fuids, None

    def callback(self, answer):
        fuids, error = self.get_result(answer)
        self.real_callback.callback(fuids, error)

class GetGroupMembersCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            uids = answer.get("uids", [])
            return uids, None

    def callback(self, answer):
        uids, error = self.get_result(answer)
        self.real_callback.callback(uids, error)

class IsGroupMemberCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            ok = answer.get("ok", False)
            return ok, None

    def callback(self, answer):
        ok, error = self.get_result(answer)
        self.real_callback.callback(ok, error)

class GetUserGroupsCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            gids = answer.get("gids", [])
            return gids, None

    def callback(self, answer):
        gids, error = self.get_result(answer)
        self.real_callback.callback(gids, error)

class IsBanOfGroupCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            ok = answer.get("ok", False)
            return ok, None

    def callback(self, answer):
        ok, error = self.get_result(answer)
        self.real_callback.callback(ok, error)

class GetGroupInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, None, QuestError(answer.error_code, answer.error_message)
        else:
            oinfo = answer.get("oinfo", None)
            pinfo = answer.get("pinfo", None)
            return oinfo, pinfo, None

    def callback(self, answer):
        oinfo, pinfo, error = self.get_result(answer)
        self.real_callback.callback(oinfo, pinfo, error)

class IsBanOfRoomCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            ok = answer.get("ok", False)
            return ok, None

    def callback(self, answer):
        ok, error = self.get_result(answer)
        self.real_callback.callback(ok, error)

class GetRoomInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, None, QuestError(answer.error_code, answer.error_message)
        else:
            oinfo = answer.get("oinfo", None)
            pinfo = answer.get("pinfo", None)
            return oinfo, pinfo, None

    def callback(self, answer):
        oinfo, pinfo, error = self.get_result(answer)
        self.real_callback.callback(oinfo, pinfo, error)

class DataGetCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, QuestError(answer.error_code, answer.error_message)
        else:
            value = answer.get("val", None)
            return value, None

    def callback(self, answer):
        value, error = self.get_result(answer)
        self.real_callback.callback(value, error)