# RTM Server-End Python SDK Files API Docs

# Index

[TOC]

## API

### file_token

##### get file token

```
file_token(from_uid, cmd, to_uids = None, to_uid = None, rid = None, gid = None, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* cmd: **(Required | str)**  send file type, (sendfile/sendfiles/sendroomfile/sendgroupfile/broadcastfile)
* to_uid: **(Optional | int)**  cmd = sendfile required
* to_uids: **(Optional | [int])**  cmd = sendfiles required
* rid: **(Optional | int)**  cmd = sendroomfile required
* gid: **(Optional | int)**  cmd = sendgroupfile required
* callback: **(Optional | a sub-class of FileTokenCallback )**  used in async implementation

```python
class FileTokenCallback(object):
    def callback(self, token, endpoint, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(FileTokenCallback)** transcribe result
  * error_code:  **(int)**   the error_code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### send_file

##### send a P2P file

```
send_file(from_uid, to_uid, mtype, file, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* to_uid: **(Required | int)**  to user id
* file: **(Required | str)**  file content
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error_code:  **(int)**   the error_code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### send_files

##### send a muti-user file

```
send_files(from_uid, to_uids, mtype, file, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* to_uids: **(Required | [int])**  to user id list
* file: **(Required | str)**  file content
* attrs: **(Required | str)**  message attributes
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error_code:  **(int)**   the error when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### send_group_file

##### send a group file

```
send_group_file(from_uid, gid, mtype, file, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* gid: **(Required | int)**  group id
* file: **(Required | str)**  file content
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error_code:  **(int)**   the error when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### send_room_file

##### send a room file

```
send_room_file(from_uid, rid, mtype, file, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* rid: **(Required | int)**  room id
* file: **(Required | str)**  file content
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error_code:  **(int)**   the error when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### broadcast_file

##### broadcast file

```
broadcast_file(from_uid, mtype, file, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* file: **(Required | str)**  file content
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error_code:  **(int)**   the error when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



