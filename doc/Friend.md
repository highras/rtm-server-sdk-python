# RTM Server-End Python SDK Friend API Docs

# Index

[TOC]

## API

### add_friends

##### add friends

```
add_friends(uid, friends, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* friends: **(Optional | [int])**  friend user id list
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



### delete_friends

##### delete friends

```
delete_friends(self, uid, friends, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* friends: **(Optional | [int])**  friend user id list
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



### get_friends

##### get user friends

```
get_friends(uid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* callback: **(Optional | a sub-class of GetFriendsCallback )**  used in async implementation

```python
class GetFriendsCallback(object):
    def callback(self, uids, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * uids:  **([])** user list
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### is_friend

##### check is friend

```
is_friend(uid, fuid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* fuid: **(Required | int)**  friend user id
* callback: **(Optional | a sub-class of IsFriendCallback )**  used in async implementation

```python
class IsFriendCallback(object):
    def callback(self, ok, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * ok:  **(bool)** is friend
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### is_friends

##### check is friends

```
is_friends(self, uid, fuids, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* fuids: **(Required | [int])**  friend user id
* callback: **(Optional | a sub-class of IsFriendsCallback )**  used in async implementation

```python
class IsFriendsCallback(object):
    def callback(self, fuids, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * fuids:  **([int])** friend user id list
  * error:  **(QuestError)**   the error when quest is fail, or None when success





