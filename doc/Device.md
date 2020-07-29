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





