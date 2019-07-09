# rtm-server-sdk-python

#### 例子 ####
```python

client = RTMServerClient(11000006, 'xxxxx-xxxx-xxxx-xxx-xxxxxx', '52.83.245.22:13315')

class MyDoneCallback(DoneCallback):
    def done(self):
        print("done")
    
    def onException(self, exception):
        print repr(exception)

client.sendMessage(1, 2, 51, "test msg", "test attrs", MyDoneCallback())
```

#### API ####

* __init__(self, pid, secretKey, endpoint, timeout=5)    
* close(self)
* setConnectionConnectedCallback(self, cb)
* setConnectionWillCloseCallback(self, cb)
* enableEncryptor(self, peerPubData) 

```
以下请求类接口，均有同步与异步两个版本

对于异步版本，sendMessage、sendMessages、sendGroupMessage、sendRoomMessage、broadcastMessage、addfriends、deleteFriends、deleteGroupMembers、deleteGroup、addGroupBan、removeGroupBan、addRoomBan、removeRoomBan、addProjectBlack、removeProjectBlack
这几个接口cb参数类型为DoneCallback的派生类
其他接口cb参数类型为其同名的Callback派生类（如isGroupMember，则为IsGroupMemberCallback）

对于同步版本，当发生异常时会抛出异常，当正常时返回该接口特有的数据类型，可参考对应异步版本Callback中done方法参数
```

* sendMessage(self, fromUid, toUid, mtype, msg, attrs, cb)  
* sendMessagesSync(self, fromUid, toUids, mtype, msg, attrs) 
* sendGroupMessage(self, fromUid, gid, mtype, msg, attrs, cb)
* sendGroupMessageSync(self, fromUid, gid, mtype, msg, attrs)
* sendRoomMessage(self, fromUid, rid, mtype, msg, attrs, cb)
* sendRoomMessageSync(self, fromUid, rid, mtype, msg, attrs)
* broadcastMessage(self, fromUid, mtype, msg, attrs, cb) 
* broadcastMessageSync(self, fromUid, mtype, msg, attrs) 
* addfriends(self, uid, friends, cb)
* addfriendsSync(self, uid, friends) 
* deleteFriends(self, uid, friends, cb)
* deleteFriendsSync(self, uid, friends)
* getFriends(self, uid, cb) 
* getFriendsSync(self, uid)
* isFriend(self, uid, fuid, cb)
* isFriendSync(self, uid, fuid)
* isFriends(self, uid, fuids, cb)
* isFriendsSync(self, uid, fuids)
* addGroupMembers(self, gid, uids, cb)
* addGroupMembersSync(self, gid, uids)
* deleteGroupMembers(self, gid, uids, cb)
* deleteGroupMembersSync(self, gid, uids)
* deleteGroup(self, gid)
* deleteGroupSync(self, gid)
* getGroupMembers(self, gid, cb)
* getGroupMembersSync(self, gid)
* isGroupMember(self, gid, uid, cb)
* isGroupMemberSync(self, gid, uid)
* getUserGroups(self, uid, cb)
* getUserGroupsSync(self, uid)
* getToken(self, uid, cb)
* getTokenSync(self, uid)
* getOnlineUsers(self, uids, cb)
* getOnlineUsersSync(self, uids)
* addGroupBan(self, gid, uid, btime, cb)
* addGroupBanSync(self, gid, uid, btime)
* removeGroupBan(self, gid, uid, cb)
* removeGroupBanSync(self, gid, uid)
* addRoomBan(self, rid, uid, btime, cb)
* addRoomBanSync(self, rid, uid, btime)
* removeRoomBan(self, rid, uid, cb)
* removeRoomBanSync(self, rid, uid)
* addProjectBlack(self, uid, btime, cb)
* addProjectBlackSync(self, uid, btime)
* removeProjectBlack(self, uid, cb)
* removeProjectBlackSync(self, uid)
* isBanOfGroup(self, gid, uid, cb)
* isBanOfGroupSync(self, gid, uid)
* isBanOfRoom(self, rid, uid, cb)
* isBanOfRoomSync(self, rid, uid)
* isProjectBlack(self, uid, cb)
* isProjectBlackSync(self, uid)



























