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
    def callback(self, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



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
    def callback(self, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



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
    def callback(self, uids, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * uids:  **([])** user list
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



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
    def callback(self, ok, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * ok:  **(bool)** is friend
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



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
    def callback(self, fuids, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * fuids:  **([int])** friend user id list
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success


### add_blacks

##### add blacks

```
add_blacks(uid, blacks, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* blacks: **(Optional | [int])**  black user id list
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### delete_blacks

##### delete blacks

```
delete_blacks(self, uid, blacks, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* blacks: **(Optional | [int])**  black friend user id list
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_blacks

##### get user's black list

```
get_blacks(uid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* callback: **(Optional | a sub-class of GetBlacksCallback )**  used in async implementation

```python
class GetBlacksCallback(object):
    def callback(self, uids, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * uids:  **([])** user list
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### is_black

##### check is black

```
is_black(uid, buid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* buid: **(Required | int)**  other user id
* callback: **(Optional | a sub-class of IsBlackCallback )**  used in async implementation

```python
class IsBlackCallback(object):
    def callback(self, ok, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * ok:  **(bool)** is friend
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### is_blacks

##### check is blacks

```
is_blacks(self, uid, buids, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* buids: **(Required | [int])**  blacks user id
* callback: **(Optional | a sub-class of IsFriendsCallback )**  used in async implementation

```python
class IsBlacksCallback(object):
    def callback(self, buids, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * fuids:  **([int])** friend user id list
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success





