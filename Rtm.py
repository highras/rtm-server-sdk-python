# coding: utf-8
from __future__ import with_statement

import time
import hashlib
import threading
import Fpnn

__all__ = ('RTMServerClient', 'DoneCallback', 'GetFriendsCallback', 'IsFriendCallback', 'IsFriendsCallback', 'GetGroupMembersCallback', 'IsGroupMemberCallback', 'GetUserGroupsCallback', 'GetTokenCallback', 'GetOnlineUsersCallback', 'IsBanOfGroupCallback', 'IsBanOfRoomCallback', 'IsProjectBlackCallback', 'GetPushNameCallback', 'GetGeoCallback', 'GetGeosCallback')

class DoneCallback:
    def done(self):
        pass
    def onException(self, exception):
        pass

class DoneCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            self.cb.done()
        else:
            self.cb.onException(exception)

class GetFriendsCallback:
    def done(self, uids):
        pass

    def onException(self, exception):
        pass

class GetFriendsCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('uids'):
                self.cb.done(answer['uids'])
            else:
                self.cb.done([])
        else:
            self.cb.onException(exception)

class IsFriendCallback:
    def done(self, ok):
        pass

    def onException(self, exception):
        pass

class IsFriendCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('ok'):
                self.cb.done(bool(answer['ok']))
            else:
                self.cb.done(False)
        else:
            self.cb.onException(exception)

class IsFriendsCallback:
    def done(self, fuids):
        pass

    def onException(self, exception):
        pass

class IsFriendsCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('fuids'):
                self.cb.done(answer['fuids'])
            else:
                self.cb.done([])
        else:
            self.cb.onException(exception)

class GetGroupMembersCallback:
    def done(self, uids):
        pass

    def onException(self, exception):
        pass

class GetGroupMembersCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('uids'):
                self.cb.done(answer['uids'])
            else:
                self.cb.done([])
        else:
            self.cb.onException(exception)

class IsGroupMemberCallback:
    def done(self, ok):
        pass

    def onException(self, exception):
        pass

class IsGroupMemberCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('ok'):
                self.cb.done(bool(answer['ok']))
            else:
                self.cb.done(False)
        else:
            self.cb.onException(exception)

class GetUserGroupsCallback:
    def done(self, gids):
        pass

    def onException(self, exception):
        pass

class GetUserGroupsCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('gids'):
                self.cb.done(answer['gids'])
            else:
                self.cb.done([])
        else:
            self.cb.onException(exception)

class GetTokenCallback:
    def done(self, token):
        pass

    def onException(self, exception):
        pass

class GetTokenCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('token'):
                self.cb.done(answer['token'])
            else:
                self.cb.done('')
        else:
            self.cb.onException(exception)

class GetOnlineUsersCallback:
    def done(self, uids):
        pass

    def onException(self, exception):
        pass

class GetOnlineUsersCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('uids'):
                self.cb.done(answer['uids'])
            else:
                self.cb.done([])
        else:
            self.cb.onException(exception)

class IsBanOfGroupCallback:
    def done(self, ok):
        pass

    def onException(self, exception):
        pass

class IsBanOfGroupCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('ok'):
                self.cb.done(bool(answer['ok']))
            else:
                self.cb.done(False)
        else:
            self.cb.onException(exception)

class IsBanOfRoomCallback:
    def done(self, ok):
        pass

    def onException(self, exception):
        pass

class IsBanOfRoomCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('ok'):
                self.cb.done(bool(answer['ok']))
            else:
                self.cb.done(False)
        else:
            self.cb.onException(exception)

class IsProjectBlackCallback:
    def done(self, ok):
        pass

    def onException(self, exception):
        pass

class IsProjectBlackCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('ok'):
                self.cb.done(bool(answer['ok']))
            else:
                self.cb.done(False)
        else:
            self.cb.onException(exception)

class GetPushNameCallback:
    def done(self, pushname):
        pass

    def onException(self, exception):
        pass

class GetPushNameCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            if answer.has_key('pushname'):
                self.cb.done(answer['pushname'])
            else:
                self.cb.done('')
        else:
            self.cb.onException(exception)

class GetGeoCallback:
    def done(self, geo):
        pass

    def onException(self, exception):
        pass

class GetGeoCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            self.cb.done(answer)
        else:
            self.cb.onException(exception)

class GetGeosCallback:
    def done(self, geos):
        pass

    def onException(self, exception):
        pass

class GetGeosCallbackInternal(Fpnn.FpnnCallback):
    def __init__(self, cb):
        self.cb = cb

    def callback(self, answer, exception):
        if exception == None:
            self.cb.done(answer)
        else:
            self.cb.onException(exception)


class RTMServerClient:
    def __init__(self, pid, secretKey, endpoint, timeout=5):
        self.midSeqLock = threading.Lock()
        self.midSeq = 0
        self.saltSeqLock = threading.Lock()
        self.saltSeq = 0
        arr = endpoint.split(':')
        self.pid = pid
        self.secretKey = secretKey
        self.client = Fpnn.TCPClient(arr[0], int(arr[1]), timeout)

    def close(self):
        self.client.close()

    def enableEncryptor(self, peerPubData):
        self.client.enableEncryptor(peerPubData)

    def genMid(self):
        with self.midSeqLock:
            self.midSeq += 1
            return (int(time.time()) << 32) + (self.midSeq & 0xffffff)

    def genSalt(self):
        with self.saltSeqLock:
            self.saltSeq += 1
            return (int(time.time()) << 32) + (self.saltSeq & 0xffffff)

    def genSign(self, salt):
        return hashlib.md5(str(self.pid) + ':' + self.secretKey + ':' +
                str(salt)).hexdigest().upper()

    def sendMessageSync(self, fromUid, toUid, mtype, msg, attrs):
        salt = self.genSalt()
        self.client.sendQuestSync('sendmsg', {
            'pid' : self.pid,
            'sign' : self.genSign(salt),
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'to' : toUid,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        })

    def sendMessage(self, fromUid, toUid, mtype, msg, attrs, cb):
        salt = self.genSalt()
        self.client.sendQuest('sendmsg', {
            'pid' : self.pid,
            'sign' : self.genSign(salt),
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'to' : toUid,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        }, DoneCallbackInternal(cb))

    def sendMessagesSync(self, fromUid, toUids, mtype, msg, attrs):
        salt = self.genSalt()
        self.client.sendQuestSync("sendmsgs", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'tos' : toUids,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        })

    def sendMessages(self, fromUid, toUids, mtype, msg, attrs, cb):
        salt = self.genSalt()
        self.client.sendQuest("sendmsgs", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'tos' : toUids,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        }, DoneCallbackInternal(cb))

    def sendGroupMessageSync(self, fromUid, gid, mtype, msg, attrs):
        salt = self.genSalt()
        self.client.sendQuestSync("sendgroupmsg", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'gid' : gid,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        })

    def sendGroupMessage(self, fromUid, gid, mtype, msg, attrs, cb):
        salt = self.genSalt()
        self.client.sendQuest("sendgroupmsg", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'gid' : gid,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        }, DoneCallbackInternal(cb))

    def sendRoomMessageSync(self, fromUid, rid, mtype, msg, attrs):
        salt = self.genSalt()
        self.client.sendQuestSync("sendroommsg", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'rid' : rid,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        })

    def sendRoomMessage(self, fromUid, rid, mtype, msg, attrs, cb):
        salt = self.genSalt()
        self.client.sendQuest("sendroommsg", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'rid' : rid,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        }, DoneCallbackInternal(cb))

    def broadcastMessageSync(self, fromUid, mtype, msg, attrs):
        salt = self.genSalt()
        self.client.sendQuestSync("broadcastmsg", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        })

    def broadcastMessage(self, fromUid, mtype, msg, attrs, cb):
        salt = self.genSalt()
        self.client.sendQuest("broadcastmsg", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'mtype' : mtype,
            'from' : fromUid,
            'mid' : self.genMid(),
            'msg' : msg,
            'attrs' : attrs
        }, DoneCallbackInternal(cb))

    def addfriendsSync(self, uid, friends):
        salt = self.genSalt()
        self.client.sendQuestSync("addfriends", {
            'pid' : self.pid,
            'sign' : self.genSign(salt),
            'salt' : salt,
            'uid' : uid,
            'friends' : friends
        })

    def addfriends(self, uid, friends, cb): 
        salt = self.genSalt()
        self.client.sendQuest("addfriends", {
            'pid' : self.pid,
            'sign' : self.genSign(salt),
            'salt' : salt,
            'uid' : uid,
            'friends' : friends
        }, DoneCallbackInternal(cb))

    def deleteFriendsSync(self, uid, friends):
        salt = self.genSalt()
        self.client.sendQuestSync("delfriends", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'friends' : friends
        })

    def deleteFriends(self, uid, friends, cb):
        salt = self.genSalt()
        self.client.sendQuest("delfriends", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'friends' : friends
        }, DoneCallbackInternal(cb))

    def getFriendsSync(self, uid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("getfriends", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        })
        if res.has_key('uids'):
            return res['uids']
        else:
            return []

    def getFriends(self, uid, cb):
        salt = self.genSalt()
        res = self.client.sendQuest("getfriends", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        }, GetFriendsCallbackInternal(cb))

    def isFriendSync(self, uid, fuid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("isfriend", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'fuid' : fuid
        })
        if res.has_key('ok'):
            return bool(res['ok'])
        else:
            return False

    def isFriend(self, uid, fuid, cb):
        salt = self.genSalt()
        self.client.sendQuest("isfriend", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'fuid' : fuid
        }, IsFriendCallbackInternal(cb))

    def isFriendsSync(self, uid, fuids):
        salt = self.genSalt()
        res = self.client.sendQuestSync("isfriends", {
            'pid' : self.pid,
            'sign' : self.genSign(salt),
            'salt' : salt,
            'uid' : uid,
            'fuids' : fuids
        })
        if res.has_key('fuids'):
            return res['fuids']
        else:
            return []

    def isFriends(self, uid, fuids, cb):
        salt = self.genSalt()
        self.client.sendQuest("isfriends", {
            'pid' : self.pid,
            'sign' : self.genSign(salt),
            'salt' : salt,
            'uid' : uid,
            'fuids' : fuids
        }, IsFriendsCallback(cb))

    def addGroupMembersSync(self, gid, uids):
        salt = self.genSalt()
        self.client.sendQuestSync("addgroupmembers", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid,
            'uids' : uids
        })

    def addGroupMembers(self, gid, uids, cb):
        salt = self.genSalt()
        self.client.sendQuest("addgroupmembers", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid,
            'uids' : uids
        }, DoneCallbackInternal(cb))

    def deleteGroupMembersSync(self, gid, uids):
        salt = self.genSalt()
        self.client.sendQuestSync("delgroupmembers", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid,
            'uids' : uids
        })

    def deleteGroupMembers(self, gid, uids, cb):
        salt = self.genSalt()
        self.client.sendQuest("delgroupmembers", {
            'pid' : self.pid,
            'sign' : self.genSign(salt),
            'salt' : salt,
            'gid' : gid,
            'uids' : uids
        }, DoneCallbackInternal(cb))

    def deleteGroupSync(self, gid):
        salt = self.genSalt()
        self.client.sendQuestSync("delgroup", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid
        })

    def deleteGroup(self, gid):
        salt = self.genSalt()
        self.client.sendQuest("delgroup", { 
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid
        }, DoneCallbackInternal(cb))

    def getGroupMembersSync(self, gid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("getgroupmembers", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid
        })
        if res.has_key('uids'):
            return res['uids']
        else:
            return []

    def getGroupMembers(self, gid, cb):
        salt = self.genSalt()
        res = self.client.sendQuest("getgroupmembers", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid
        }, GetGroupMembersCallbackInternal(cb))

    def isGroupMemberSync(self, gid, uid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("isgroupmember", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid,
            'uid' : uid
        })
        if res.has_key('ok'):
            return bool(res['ok'])
        else:
            return False

    def isGroupMember(self, gid, uid, cb):
        salt = self.genSalt()
        res = self.client.sendQuest("isgroupmember", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid,
            'uid' : uid
        }, IsGroupMemberCallbackInternal(cb))

    def getUserGroupsSync(self, uid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("getusergroups", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        })
        if res.has_key('gids'):
            return res['gids']
        else:
            return []

    def getUserGroups(self, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("getusergroups", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        }, GetUserGroupsCallbackInternal(cb))

    def getTokenSync(self, uid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("gettoken", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        })
        if res.has_key('token'):
            return res['token']
        else:
            return ''

    def getToken(self, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("gettoken", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        }, GetTokenCallbackInternal(cb))

    def getOnlineUsersSync(self, uids):
        salt = self.genSalt()
        res = self.client.sendQuestSync("getonlineusers", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uids' : uids
        })
        if res.has_key('uids'):
            return res['uids']
        else:
            return [] 

    def getOnlineUsers(self, uids, cb):
        salt = self.genSalt()
        self.client.sendQuest("getonlineusers", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uids' : uids
        }, GetOnlineUsersCallbackInternal(cb))

    def addGroupBanSync(self, gid, uid, btime):
        salt = self.genSalt()
        self.client.sendQuestSync("addgroupban", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid,
            'uid' : uid,
            'btime' : btime
        })

    def addGroupBan(self, gid, uid, btime, cb):
        salt = self.genSalt()
        self.client.sendQuest("addgroupban", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid,
            'uid' : uid,
            'btime' : btime
        }, DoneCallbackInternal(cb))

    def removeGroupBanSync(self, gid, uid):
        salt = self.genSalt()
        self.client.sendQuestSync("removegroupban", {
            'pid' :  self.pid,
            'sign' :  self.genSign(salt), 
            'salt' :  salt,
            'gid' :  gid,
            'uid' :  uid
        })

    def removeGroupBan(self, gid, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("removegroupban", {
            'pid' :  self.pid,
            'sign' :  self.genSign(salt), 
            'salt' :  salt,
            'gid' :  gid,
            'uid' :  uid
        }, DoneCallbackInternal(cb))

    def addRoomBanSync(self, rid, uid, btime):
        salt = self.genSalt()
        self.client.sendQuestSync("addroomban", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'rid' : rid,
            'uid' : uid,
            'btime' : btime
        })

    def addRoomBan(self, rid, uid, btime, cb):
        salt = self.genSalt()
        self.client.sendQuest("addroomban", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'rid' : rid,
            'uid' : uid,
            'btime' : btime
        }, DoneCallbackInternal(cb))

    def removeRoomBanSync(self, rid, uid): 
        salt = self.genSalt()
        self.client.sendQuestSync("removeroomban", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'rid' : rid,
            'uid' : uid
        })

    def removeRoomBan(self, rid, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("removeroomban", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'rid' : rid,
            'uid' : uid
        }, DoneCallbackInternal(cb))

    def addProjectBlackSync(self, uid, btime):
        salt = self.genSalt()
        self.client.sendQuestSync("addprojectblack", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'btime' : btime
        })

    def addProjectBlack(self, uid, btime, cb):
        salt = self.genSalt()
        self.client.sendQuest("addprojectblack", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'btime' : btime
        }, DoneCallbackInternal(cb))

    def removeProjectBlackSync(self, uid):
        salt = self.genSalt()
        self.client.sendQuestSync("removeprojectblack", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        })

    def removeProjectBlack(self, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("removeprojectblack", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        }, DoneCallbackInternal(cb))

    def isBanOfGroupSync(self, gid, uid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("isbanofgroup", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid,
            'uid' : uid
        })
        if res.has_key('ok'):
            return bool(res['ok'])
        else:
            return False

    def isBanOfGroup(self, gid, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("isbanofgroup", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'gid' : gid,
            'uid' : uid
        }, IsBanOfGroupCallbackInternal(cb))

    def isBanOfRoomSync(self, rid, uid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("isbanofroom", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'rid' : rid,
            'uid' : uid
        })
        if res.has_key('ok'):
            return bool(res['ok'])
        else:
            return False

    def isBanOfRoom(self, rid, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("isbanofroom", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'rid' : rid,
            'uid' : uid
        }, IsBanOfRoomCallbackInternal(cb))

    def isProjectBlackSync(self, uid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("isprojectblack", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        })
        if res.has_key('ok'):
            return bool(res['ok'])
        else:
            return False

    def isProjectBlack(self, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("isprojectblack", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        }, IsProjectBlackCallbackInternal(cb))

    def setPushNameSync(self, uid, pushname):
        salt = self.genSalt()
        self.client.sendQuestSync("setpushname", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'pushname' : pushname
        })

    def setPushName(self, uid, pushname, cb):
        salt = self.genSalt()
        self.client.sendQuest("setpushname", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'pushname' : pushname
        }, DoneCallbackInternal(cb))

    def getPushNameSync(self, uid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("getpushname", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        })
        if res.has_key('pushname'):
            return res['pushname']
        else:
            return ''

    def getPushName(self, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("getpushname", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        }, GetPushNameCallbackInternal(cb))

    def setGeoSync(self, uid, lat, lng):
        salt = self.genSalt()
        self.client.sendQuestSync("setgeo", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'lat' : lat,
            'lng' : lng
        })

    def setGeo(self, uid, lat, lng, cb):
        salt = self.genSalt()
        self.client.sendQuest("setgeo", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid,
            'lat' : lat,
            'lng' : lng
        }, DoneCallbackInternal(cb))

    def getGeoSync(self, uid):
        salt = self.genSalt()
        res = self.client.sendQuestSync("getgeo", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        })
        return res

    def getGeo(self, uid, cb):
        salt = self.genSalt()
        self.client.sendQuest("getgeo", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uid' : uid
        }, GetGeoCallbackInternal(cb))

    def getGeosSync(self, uids):
        salt = self.genSalt()
        res = self.client.sendQuestSync("getgeos", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uids' : uids
        })
        return res

    def getGeos(self, uids, cb):
        salt = self.genSalt()
        self.client.sendQuest("getgeos", {
            'pid' : self.pid,
            'sign' : self.genSign(salt), 
            'salt' : salt,
            'uids' : uids
        }, GetGeosCallbackInternal(cb))

