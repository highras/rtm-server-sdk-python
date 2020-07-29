# RTM Server-End Python SDK User API Docs

# Index

[TOC]

## API

### kickout

##### kickout a login user

```
kickout(uid, ce = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  the user id
* ce:  **(Optional | string )** the rtm endpoint of the user, used for multi-user login 
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



### get_online_users

##### get online users

```
get_online_users(uids, callback = None, timeout = 0)
```

#### params:

* uids: **(Required | [int])**  uid list
* callback: **(Optional | a sub-class of GetOnlineUsersCallback )**  used in async implementation

```python
class GetOnlineUsersCallback(object):
    def callback(self, uids, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * uids:  **([int])** online uids result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### add_project_black

##### add user to project black list

```
add_project_black(uid, btime, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* btime: **(Required | int)**  ban time in seconds
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



### remove_project_black

##### remove user from project black list

```
remove_project_black(uid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
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



### is_project_black

##### check user is in project black list

```python
is_project_black(uid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* callback: **(Optional | a sub-class of IsProjectBlackCallback )**  used in async implementation

```python
class IsProjectBlackCallback(object):
    def callback(self, ok, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * ok:  **(bool)** is in peoject black
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### set_user_info

##### set user public and private info

```
set_user_info(uid, oinfo = None, pinfo = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* oinfo: **(Optional | str)**  public info
* pinfo: **(Optional | str)**  private info
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



### get_user_info

##### get user public and private info

```
get_user_info(uid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* callback: **(Optional | a sub-class of GetUserInfoCallback )**  used in async implementation

```python
class GetUserInfoCallback(object):
    def callback(self, oinfo, pinfo, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * oinfo:  **(int)** public info
  * pinfo:  **(int)** private info
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_user_open_info

##### get user public info

```
get_user_open_info(uids, callback = None, timeout = 0)
```

#### params:

* uids: **(Required | [int])**  user id list
* callback: **(Optional | a sub-class of GetUserOpenInfoCallback )**  used in async implementation

```python
class GetUserOpenInfoCallback(object):
    def callback(self, info, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * info:  **(dict)** public info
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success

