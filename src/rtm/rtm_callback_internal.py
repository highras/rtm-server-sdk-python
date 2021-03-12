import sys
sys.path.append("..")
from fpnn import *
from .rtm_callback import *
from .rtm_server_structures import *

class GetTokenCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            token = answer.get("token", None)
            if token == None:
                return None, RTM_ERROR.RTM_EC_UNKNOWN_ERROR.value
            else:
                return token, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        token, error_code = self.get_result(answer)
        self.real_callback.callback(token, error_code)

class BasicCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return answer.error_code
        else:
            return FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        error_code = self.get_result(answer)
        self.real_callback.callback(error_code)

class ListenCallbackInternal(BasicCallbackInternal):
    def __init__(self, real_callback, client, listen_status):
        BasicCallbackInternal.__init__(self, real_callback)
        self.client = client
        self.listen_status = listen_status

    def get_result(self, answer):
        if answer.is_error():
            return answer.error_code
        else:
            self.client.listen_status_info = self.listen_status
            return FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        error_code = self.get_result(answer)
        self.real_callback.callback(error_code)

class SendMessageCallbackInternal(QuestCallback):
    def __init__(self, real_callback, mid):
        self.real_callback = real_callback
        self.mid = mid

    def get_result(self, answer):
        if answer.is_error():
            return None, None, answer.error_code
        else:
            mtime = answer.get("mtime", None)
            if mtime == None:
                return self.mid, None, RTM_ERROR.RTM_EC_UNKNOWN_ERROR.value
            else:
                return self.mid, mtime, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        mid, mtime, error_code = self.get_result(answer)
        self.real_callback.callback(mid, mtime, error_code)

class GetGroupMessageCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = HistoryMessageResult()
            result.count = answer.get("num", 0)
            result.last_cursor_id = answer.get("lastid", 0)
            result.begin_msec = answer.get("begin", 0)
            result.end_msec = answer.get("end", 0)
            msgs = answer.get("msgs", [])
            for m in msgs:
                if len(m) != 8:
                    continue
                msg = HistoryMessage()
                msg.cursor_id = m[0]
                msg.from_uid = m[1]
                msg.message_type = m[2]
                msg.message_id = m[3]
                msg.message = m[5]
                msg.attrs = m[6]
                msg.modified_time = m[7]

                if msg.message_type >= 40 and msg.message_type <= 50:
                    msg = RTMServerClient.build_file_info(msg)

                result.messages.append(msg)
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)

class GetRoomMessageCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = HistoryMessageResult()
            result.count = answer.get("num", 0)
            result.last_cursor_id = answer.get("lastid", 0)
            result.begin_msec = answer.get("begin", 0)
            result.end_msec = answer.get("end", 0)
            msgs = answer.get("msgs", [])
            for m in msgs:
                if len(m) != 8:
                    continue
                msg = HistoryMessage()
                msg.cursor_id = m[0]
                msg.from_uid = m[1]
                msg.message_type = m[2]
                msg.message_id = m[3]
                msg.message = m[5]
                msg.attrs = m[6]
                msg.modified_time = m[7]

                if msg.message_type >= 40 and msg.message_type <= 50:
                    msg = RTMServerClient.build_file_info(msg)

                result.messages.append(msg)
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)

class GetBroadcastMessageCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = HistoryMessageResult()
            result.count = answer.get("num", 0)
            result.last_cursor_id = answer.get("lastid", 0)
            result.begin_msec = answer.get("begin", 0)
            result.end_msec = answer.get("end", 0)
            msgs = answer.get("msgs", [])
            for m in msgs:
                if len(m) != 8:
                    continue
                msg = HistoryMessage()
                msg.cursor_id = m[0]
                msg.from_uid = m[1]
                msg.message_type = m[2]
                msg.message_id = m[3]
                msg.message = m[5]
                msg.attrs = m[6]
                msg.modified_time = m[7]

                if msg.message_type >= 40 and msg.message_type <= 50:
                    msg = RTMServerClient.build_file_info(msg)

                result.messages.append(msg)
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)

class GetP2PMessageCallbackInternal(QuestCallback):
    def __init__(self, selfUid, otherUid, real_callback):
        self.selfUid = selfUid
        self.otherUid = otherUid
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = HistoryMessageResult()
            result.count = answer.get("num", 0)
            result.last_cursor_id = answer.get("lastid", 0)
            result.begin_msec = answer.get("begin", 0)
            result.end_msec = answer.get("end", 0)
            msgs = answer.get("msgs", [])
            for m in msgs:
                if len(m) != 8:
                    continue
                msg = HistoryMessage()
                msg.cursor_id = m[0]
                direction = m[1]
                if direction == 1:
                    msg.from_uid = self.selfUid
                    msg.to_id = self.otherUid
                else:
                    msg.from_uid = self.otherUid
                    msg.to_id = self.selfUid
                msg.message_type = m[2]
                msg.message_id = m[3]
                msg.message = m[5]
                msg.attrs = m[6]
                msg.modified_time = m[7]

                if msg.message_type >= 40 and msg.message_type <= 50:
                    msg = RTMServerClient.build_file_info(msg)

                result.messages.append(msg)
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)

class GetMessageInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = RetrievedMessage()
            result.cursor_id = answer.get("id", 0)
            result.message_type = answer.get("mtype", 0)
            result.message = answer.get("msg", str())
            result.attrs = answer.get("attrs", str())
            result.modified_time = answer.get("mtime", 0)
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)

class TranslateCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = TranslateResult()
            result.source = answer.get("source", str())
            result.target = answer.get("target", str())
            result.source_text = answer.get("sourceText", str())
            result.target_text = answer.get("targetText", str())
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)

class TextCheckCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = TextCheckResult()
            result.result = answer.get("result", 0)
            result.text = answer.get("text", str())
            result.tags = answer.get("tags", [])
            result.wlist = answer.get("wlist", [])
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)


class CheckCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = CheckResult()
            result.result = answer.get("result", 0)
            result.tags = answer.get("tags", [])
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)

class SpeechToTextCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = SpeechToTextResult()
            result.text = answer.get("text", str())
            result.lang = answer.get("lang", str())
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)

class FileTokenCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, None, answer.error_code
        else:
            token = answer.get("token", str())
            endpoint = answer.get("endpoint", str())
            return token, endpoint, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        token, endpoint, error_code = self.get_result(answer)
        self.real_callback.callback(token, endpoint, error_code)
        

class SendFileCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            mtime = answer.get("mtime", 0)
            return mtime, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        mtime, error_code = self.get_result(answer)
        self.real_callback.callback(mtime, error_code)

class GetOnlineUsersCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            uids = answer.get("uids", [])
            return uids, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        uids, error_code = self.get_result(answer)
        self.real_callback.callback(uids, error_code)

class IsProjectBlackCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            ok = answer.get("ok", False)
            return ok, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        ok, error_code = self.get_result(answer)
        self.real_callback.callback(ok, error_code)

class GetUserInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, None, answer.error_code
        else:
            oinfo = answer.get("oinfo", None)
            pinfo = answer.get("pinfo", None)
            return oinfo, pinfo, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        oinfo, pinfo, error_code = self.get_result(answer)
        self.real_callback.callback(oinfo, pinfo, error_code)

class GetUserOpenInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            info = answer.get("info", {})
            return info, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        info, error_code = self.get_result(answer)
        self.real_callback.callback(info, error_code)

class GetFriendsCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            uids = answer.get("uids", [])
            return uids, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        uids, error_code = self.get_result(answer)
        self.real_callback.callback(uids, error_code)

class IsFriendCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            ok = answer.get("ok", False)
            return ok, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        ok, error_code = self.get_result(answer)
        self.real_callback.callback(ok, error_code)

class IsFriendsCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            fuids = answer.get("fuids", [])
            return fuids, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        fuids, error_code = self.get_result(answer)
        self.real_callback.callback(fuids, error_code)

class GetBlacksCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            uids = answer.get("uids", [])
            return uids, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        uids, error_code = self.get_result(answer)
        self.real_callback.callback(uids, error_code)

class IsBlackCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            ok = answer.get("ok", False)
            return ok, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        ok, error_code = self.get_result(answer)
        self.real_callback.callback(ok, error_code)

class IsBlacksCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            fuids = answer.get("buids", [])
            return fuids, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        fuids, error_code = self.get_result(answer)
        self.real_callback.callback(fuids, error_code)

class GetGroupMembersCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            uids = answer.get("uids", [])
            return uids, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        uids, error_code = self.get_result(answer)
        self.real_callback.callback(uids, error_code)

class GetRoomMembersCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            uids = answer.get("uids", [])
            return uids, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        uids, error_code = self.get_result(answer)
        self.real_callback.callback(uids, error_code)

class GetRoomCountCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            count = dict()
            count_dict = answer.get("cn", dict())
            for key in count_dict:
                count[int(key)] = count_dict[key]
            return count, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        count, error_code = self.get_result(answer)
        self.real_callback.callback(count, error_code)

class IsGroupMemberCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            ok = answer.get("ok", False)
            return ok, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        ok, error_code = self.get_result(answer)
        self.real_callback.callback(ok, error_code)

class GetUserGroupsCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            gids = answer.get("gids", [])
            return gids, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        gids, error_code = self.get_result(answer)
        self.real_callback.callback(gids, error_code)

class IsBanOfGroupCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            ok = answer.get("ok", False)
            return ok, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        ok, error_code = self.get_result(answer)
        self.real_callback.callback(ok, error_code)

class GetGroupInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, None, answer.error_code
        else:
            oinfo = answer.get("oinfo", None)
            pinfo = answer.get("pinfo", None)
            return oinfo, pinfo, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        oinfo, pinfo, error_code = self.get_result(answer)
        self.real_callback.callback(oinfo, pinfo, error_code)

class IsBanOfRoomCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            ok = answer.get("ok", False)
            return ok, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        ok, error_code = self.get_result(answer)
        self.real_callback.callback(ok, error_code)

class GetRoomInfoCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, None, answer.error_code
        else:
            oinfo = answer.get("oinfo", None)
            pinfo = answer.get("pinfo", None)
            return oinfo, pinfo, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        oinfo, pinfo, error_code = self.get_result(answer)
        self.real_callback.callback(oinfo, pinfo, error_code)

class DataGetCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            value = answer.get("val", None)
            return value, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        value, error_code = self.get_result(answer)
        self.real_callback.callback(value, error_code)

class GetDevicePushOptionCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = GetDevicePushOptionResult()
            p2p = answer.get("p2p", dict())
            group = answer.get("group", dict())
            for key in p2p:
                result.p2p[int(key)] = p2p[key]
            for key in group:
                result.group[int(key)] = group[key]
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)

class GetMessageNumCallbackInternal(QuestCallback):
    def __init__(self, real_callback):
        self.real_callback = real_callback

    def get_result(self, answer):
        if answer.is_error():
            return None, answer.error_code
        else:
            result = GetMessageNumResult()
            result.sender = answer.get("sender", 0)
            result.num = answer.get("num", 0)
            return result, FPNN_ERROR.FPNN_EC_OK

    def callback(self, answer):
        result, error_code = self.get_result(answer)
        self.real_callback.callback(result, error_code)
