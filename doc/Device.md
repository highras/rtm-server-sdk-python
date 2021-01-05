# RTM Server-End Python SDK Device API Docs

# Index

[TOC]

## API

### add_device

##### add a device token (for mobile notification)

```
add_device(uid, app_type, device_token, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  the user id
* app_type: **(Required | string) ** apns or pcm
* device_token: **(Required | string)** device token
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### remove_device

##### remove a device token (for mobile notification)

```
remove_device(uid, device_token, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  the user id
* device_token: **(Required | string)** device token
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success


### add device push option (set some users not to accept notification push)

##### add device push option

```
add_device_push_option(uid, option_type, xid, mtypes = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  the user id
* option_type: **(Required | int) ** 0 : for p2p, 1: for group
* xid: **(Required | int)** user id for p2p, group id for group
* mtypes: **(Optional | list<int>)** if mtypes = [], all mtype will not be pushd, if mtypes != [], specified mtype will not be pushd
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### remove device push option

##### remove device push option

```
remove_device_push_option(uid, option_type, xid, mtypes = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  the user id
* option_type: **(Required | int) ** 0 : for p2p, 1: for group
* xid: **(Required | int)** user id for p2p, group id for group
* mtypes: **(Optional | list<int>)** if mtypes != [], specified mtype will be removed, if mtypes = [] means remove all mtypes, but previously added mtype separately will not be removed
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class BasicCallback(object):
    def callback(self, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success


### get device push option

##### get device push option

```
ge†_device_push_option(uid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  the user id
* callback: **(Optional | a sub-class of GetDevicePushOptionCallback )**  used in async implementation

```python
class GetDevicePushOptionCallback(object):
    def callback(self, result, error):
        pass

# result is:
class GetDevicePushOptionResult(object):
    def __init__(self):
        self.p2p = dict()
        self.group = dict()
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:
    * result.p2p:  **(dict)**  uid => set<mtype>  note:  in mtypes set, 0 means all mtype
    * result.group:  **(dict)**  gid => set<mtype> note:  in mtypes set, 0 means all mtype
  * error_code:  **(int)**   the error when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success