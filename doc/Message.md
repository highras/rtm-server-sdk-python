# RTM Server-End Python SDK Message API Docs

# Index

[TOC]

## API

### send_message

##### send a P2P message

```
send_message(mtype, from_uid, to_uid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* to_uid: **(Required | int)**  to user id
* message: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### send_messages

##### send a muti-user message

```
send_messages(mtype, from_uid, to_uids, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* to_uids: **(Required | [int])**  to user id list
* message: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### send_group_message

##### send a group message

```
send_group_message(mtype, from_uid, gid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* gid: **(Required | int)**  group id
* message: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### send_room_message

##### send a room message

```
send_room_message(mtype, from_uid, rid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* rid: **(Required | int)**  room id
* message: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### broadcast_message

##### broadcast message

```
broadcast_message(mtype, from_uid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* mtype: **(Required | int)**  message type, please use >50 mtype values
* from_uid: **(Required | int)**  from user id
* message: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_group_message

##### get group message history

```
get_group_message(uid, gid, desc, num, begin = None, end = None, lastid = None, mtypes = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* gid: **(Required | int)**  group id
* num: **(Require | int)** get num
* desc: **(Required | bool)**  False: turn pages in order from the timestamp of begin, True: turn pages in reverse order from the timestamp of end
* begin: **(Required | str)** begin timestamp in microseconds (>=)，default is None
* end: **(Optional | int)**  end timestamp in microseconds (<=)，default is None
* lastid: **(Optional | int)**  last message id，default is None
* mtypes: **(Optional | [int])**  the mtype list of message, default is None
* callback: **(Optional | a sub-class of GetGroupMessageCallback )**  used in async implementation

```python
class GetGroupMessageCallback(object):
    def callback(self, result, error_code):
        pass
```

#### callback params: 
 * result is: HistoryMessageResult Please refer [RTM Structures](Structures.md).

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(HistoryMessageResult)** message result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_room_message

##### get room message history

```
get_room_message(uid, rid, desc, num, begin = None, end = None, lastid = None, mtypes = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* rid: **(Required | int)**  room id
* desc: **(Required | bool)**  False: turn pages in order from the timestamp of begin, True: turn pages in reverse order from the timestamp of end
* num: **(Require | int)** get num
* begin: **(Required | str)** begin timestamp in microseconds (>=)，default is None
* end: **(Optional | int)**  end timestamp in microseconds (<=)，default is None
* lastid: **(Optional | int)**  last message id，default is None
* mtypes: **(Optional | [int])**  the mtype list of message, default is None
* callback: **(Optional | a sub-class of GetRoomMessageCallback )**  used in async implementation

```python
class GetRoomMessageCallback(object):
    def callback(self, result, error_code):
        pass
```

#### callback params: 
 * result is: HistoryMessageResult Please refer [RTM Structures](Structures.md).

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(HistoryMessageResult)** message result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_broadcast_message

##### get broadcast message history

```
get_broadcast_message(uid, desc, num, begin = None, end = None, lastid = None, mtypes = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* desc: **(Required | bool)**  False: turn pages in order from the timestamp of begin, True: turn pages in reverse order from the timestamp of end
* num: **(Require | int)** get num
* begin: **(Required | str)** begin timestamp in microseconds (>=)，default is None
* end: **(Optional | int)**  end timestamp in microseconds (<=)，default is None
* lastid: **(Optional | int)**  last message id，default is None
* mtypes: **(Optional | [int])**  the mtype list of message, default is None
* callback: **(Optional | a sub-class of GetBroadcastMessageCallback )**  used in async implementation

```python
class GetBroadcastMessageCallback(object):
    def callback(self, result, error_code):
        pass
```

#### callback params: 
 * result is: HistoryMessageResult Please refer [RTM Structures](Structures.md).

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(HistoryMessageResult)** message result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_p2p_message

##### get p2p message history

```
get_p2p_message(uid, ouid, desc, num, begin = None, end = None, lastid = None, mtypes = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* ouid: **(Required | int)**  other user id
* desc: **(Required | bool)**  False: turn pages in order from the timestamp of begin, True: turn pages in reverse order from the timestamp of end
* num: **(Require | int)** get num
* begin: **(Required | str)** begin timestamp in microseconds (>=)，default is None
* end: **(Optional | int)**  end timestamp in microseconds (<=)，default is None
* lastid: **(Optional | int)**  last message id，default is None
* mtypes: **(Optional | [int])**  the mtype list of message, default is None
* callback: **(Optional | a sub-class of GetP2PMessageCallback )**  used in async implementation

```python
class GetP2PMessageCallback(object):
    def callback(self, result, error_code):
        pass
```

#### callback params: 
 * result is: HistoryMessageResult Please refer [RTM Structures](Structures.md).

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(HistoryMessageResult)** message result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### delete_p2p_message

##### delete p2p message history

```
delete_p2p_message(mid, from_uid, to_uid, callback = None, timeout = 0)
```

#### params:

* mid: **(Required | int)**  message id
* from_uid: **(Required | int)**  from user id
* to_uid: **(Required | int)**  to user id
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



### delete_group_message

##### delete group message history

```
delete_group_message(mid, from_uid, gid, callback = None, timeout = 0)
```

#### params:

* mid: **(Required | int)**  message id
* from_uid: **(Required | int)**  from user id
* gid: **(Required | int)**  group id
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



### delete_room_message

##### delete room message history

```
delete_room_message(mid, from_uid, rid, callback = None, timeout = 0)
```

#### params:

* mid: **(Required | int)**  message id
* from_uid: **(Required | int)**  from user id
* rid: **(Required | int)**  room id
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



### delete_broadcast_message

##### delete broadcast message history

```
delete_broadcast_message(mid, from_uid, callback = None, timeout = 0)
```

#### params:

* mid: **(Required | int)**  message id
* from_uid: **(Required | int)**  from user id
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



### get_p2p_message_info

##### get p2p message info

```
get_p2p_message_info(mid, from_uid, to_uid, callback = None, timeout = 0)
```

#### params:

* mid: **(Required | int)**  message id
* from_uid: **(Required | int)**  from user id
* to_uid: **(Required | int)**  to user id
* callback: **(Optional | a sub-class of GetMessageInfoCallback )**  used in async implementation

```python
class GetMessageInfoCallback(object):
    def callback(self, result, error_code):
        pass
```

#### callback params: 
 * result is: RetrievedMessage Please refer [RTM Structures](Structures.md).

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(RetrievedMessage)** message result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_group_message_info

##### get group message info

```
get_group_message_info(mid, from_uid, gid, callback = None, timeout = 0)
```

#### params:

* mid: **(Required | int)**  message id
* from_uid: **(Required | int)**  from user id
* gid: **(Required | int)**  group id
* callback: **(Optional | a sub-class of GetMessageInfoCallback )**  used in async implementation

```python
class GetMessageInfoCallback(object):
    def callback(self, result, error_code):
        pass
```

#### callback params: 
 * result is: RetrievedMessage Please refer [RTM Structures](Structures.md).

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(RetrievedMessage)** message result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_room_message_info

##### get room message info

```
get_room_message_info(mid, from_uid, rid, callback = None, timeout = 0)
```

#### params:

* mid: **(Required | int)**  message id
* from_uid: **(Required | int)**  from user id
* rid: **(Required | int)**  room id
* callback: **(Optional | a sub-class of GetMessageInfoCallback )**  used in async implementation

```python
class GetMessageInfoCallback(object):
    def callback(self, result, error_code):
        pass
```

#### callback params: 
 * result is: RetrievedMessage Please refer [RTM Structures](Structures.md).

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(RetrievedMessage)** message result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_broadcast_message_info

##### get broadcast message info

```
get_broadcast_message_info(self, mid, from_uid, callback = None, timeout = 0)
```

#### params:

* mid: **(Required | int)**  message id
* from_uid: **(Required | int)**  from user id
* callback: **(Optional | a sub-class of GetMessageInfoCallback )**  used in async implementation

```python
class GetMessageInfoCallback(object):
    def callback(self, result, error_code):
        pass
```

#### callback params: 
 * result is: RetrievedMessage Please refer [RTM Structures](Structures.md).

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(RetrievedMessage)** message result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success


### get_message_num

##### get message num

```
get_message_num(message_type, xid, mtypes = None, begin = None, end = None, callback = None, timeout = 0)
```

#### params:

* message_type: **(Required | int)**  2: group, 3: room
* xid: **(Required | int)**  group id or room id
* mtypes: **(Optional | [int])**  mtypes list
* begin: **(Optional | int)**  begin timestamp in milliseconds
* end: **(Optional | int)**  end timestamp in milliseconds
* callback: **(Optional | a sub-class of GetMessageInfoCallback )**  used in async implementation

```python
class GetMessageNumCallback(object):
    def callback(self, sender, num, error):
        pass

# result is:
class GetMessageNumResult(object):
    def __init__(self):
        self.sender = 0
        self.num = 0
```

#### GetMessageNumResult params: 
 * sender is: the number of senders' userIDs that has removed duplicates.
 * num is: is the message number.

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(GetMessageNumResult)** message result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success