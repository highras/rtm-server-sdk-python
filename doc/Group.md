# RTM Server-End Python SDK Group API Docs

# Index

[TOC]

## API

### add_group_members

##### add group members

```
add_group_members(gid, uids, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* uids: **(Optional | [int])**  user id list
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### delete_group_members

##### delete group members

```
delete_group_members(gid, uids, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* uids: **(Optional | [int])**  user id list
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### delete_group

##### delete group

```
delete_group(gid, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### get_group_members

##### get group members

```
get_group_members(gid, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* callback: **(Optional | a sub-class of GetGroupMembersCallback )**  used in async implementation

```python
class GetGroupMembersCallback(object):
    def callback(self, uids, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * uids:  **([])** user list
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### is_group_member

##### check is group member

```
is_group_member(gid, uid, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* uid: **(Required | int)**  user id
* callback: **(Optional | a sub-class of IsGroupMemberCallback )**  used in async implementation

```python
class IsGroupMemberCallback(object):
    def callback(self, ok, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * ok:  **(bool)** is member
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### get_user_groups

##### get user groups

```
get_user_groups(uid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* callback: **(Optional | a sub-class of GetUserGroupsCallback )**  used in async implementation

```python
class GetUserGroupsCallback(object):
    def callback(self, gids, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * gids:  **([])** group list
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### add_group_ban

##### add group ban

```
add_group_ban(gid, uid, btime, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* uid: **(Required | int)**  user id
* btime: **(Optional | int)**  ban time in second
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### remove_group_ban

##### remove group ban

```
remove_group_ban(gid, uid, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* uid: **(Required | int)**  user id
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### is_ban_of_group

##### check is ban of a group

```
is_ban_of_group(gid, uid, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* uid: **(Required | int)**  user id
* callback: **(Optional | a sub-class of IsBanOfGroupCallback )**  used in async implementation

```python
class IsBanOfGroupCallback(object):
    def callback(self, ok, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * ok:  **(bool)** is ban
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### set_group_info

##### set group public and private info

```
set_group_info(gid, oinfo = None, pinfo = None, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* oinfo: **(Optional | str)**  public info
* pinfo: **(Optional | str)**  private info
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### get_group_info

##### get group public and private info

```
get_group_info(gid, callback = None, timeout = 0)
```

#### params:

* gid: **(Required | int)**  group id
* callback: **(Optional | a sub-class of GetGroupInfoCallback )**  used in async implementation

```python
class GetGroupInfoCallback(object):
    def callback(self, oinfo, pinfo, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * oinfo:  **(int)** public info
  * pinfo:  **(int)** private info
  * error:  **(QuestError)**   the error when quest is fail, or None when success



