# RTM Server-End Python SDK Chat API Docs

# Index

[TOC]

## API

### send_chat

##### send a P2P chat

```
send_chat(from_uid, to_uid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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

#### **NOTICE:**

* in send_chat/send_chats/send_group_chat/send_room_chat/broadcast_chat, if you turn on automatic translation in value-added services, the msg params must be the original chat text



### send_chats

##### send a muti-user chat

```
send_chats(from_uid, to_uids, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_group_chat

##### send a group chat

```
send_group_chat(from_uid, gid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_room_chat

##### send a room chat

```
send_room_chat(from_uid, rid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### broadcast_chat

##### broadcast chat

```
broadcast_chat(from_uid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_audio

##### send a P2P audio

```
send_audio(from_uid, to_uid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_audios

##### send a muti-user audio

```
send_audios(from_uid, to_uids, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_group_audio

##### send a group audio

```
send_group_audio(from_uid, gid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_room_audio

##### send a room audio

```
send_room_audio(from_uid, rid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### broadcast_audio

##### broadcast audio

```
broadcast_audio(from_uid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_cmd

##### send a P2P cmd

```
send_cmd(from_uid, to_uid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_cmds

##### send a muti-user cmd

```
send_cmds(from_uid, to_uids, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_group_cmd

##### send a group cmd

```
send_group_cmd(from_uid, gid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### send_room_cmd

##### send a room cmd

```
send_room_cmd(from_uid, rid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### broadcast_cmd

##### broadcast cmd

```
broadcast_cmd(from_uid, message, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### get_group_chat

##### get group chat history

```python
get_group_chat(uid, gid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* gid: **(Required | int)**  group id
* num: **(Require | int)** get num
* desc: **(Required | bool)**  False: turn pages in order from the timestamp of begin, True: turn pages in reverse order from the timestamp of end
* begin: **(Required | str)** begin timestamp in microseconds (>=)，default is None
* end: **(Optional | int)**  end timestamp in microseconds (<=)，default is None
* lastid: **(Optional | int)**  last message id，default is None
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### get_room_chat

##### get room chat history

```
get_room_chat(uid, rid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* rid: **(Required | int)**  room id
* desc: **(Required | bool)**  False: turn pages in order from the timestamp of begin, True: turn pages in reverse order from the timestamp of end
* num: **(Require | int)** get num
* begin: **(Required | str)** begin timestamp in microseconds (>=)，default is None
* end: **(Optional | int)**  end timestamp in microseconds (<=)，default is None
* lastid: **(Optional | int)**  last message id，default is None
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### get_broadcast_chat

##### get broadcast chat history

```
get_broadcast_chat(uid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* desc: **(Required | bool)**  False: turn pages in order from the timestamp of begin, True: turn pages in reverse order from the timestamp of end
* num: **(Require | int)** get num
* begin: **(Required | str)** begin timestamp in microseconds (>=)，default is None
* end: **(Optional | int)**  end timestamp in microseconds (<=)，default is None
* lastid: **(Optional | int)**  last message id，default is None
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### get_p2p_chat

##### get p2p chat history

```
get_p2p_chat(uid, ouid, desc, num, begin = None, end = None, lastid = None, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* ouid: **(Required | int)**  other user id
* desc: **(Required | bool)**  False: turn pages in order from the timestamp of begin, True: turn pages in reverse order from the timestamp of end
* num: **(Require | int)** get num
* begin: **(Required | str)** begin timestamp in microseconds (>=)，default is None
* end: **(Optional | int)**  end timestamp in microseconds (<=)，default is None
* lastid: **(Optional | int)**  last message id，default is None
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### delete_p2p_chat

##### delete p2p chat history

```
delete_p2p_chat(mid, from_uid, to_uid, callback = None, timeout = 0)
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### delete_group_chat

##### delete group chat history

```
delete_group_chat(mid, from_uid, gid, callback = None, timeout = 0)
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### delete_room_chat

##### delete room chat history

```
delete_room_chat(mid, from_uid, rid, callback = None, timeout = 0)
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### delete_broadcast_chat

##### delete broadcast chat history

```
delete_broadcast_chat(mid, from_uid, callback = None, timeout = 0)
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### get_p2p_chat_info

##### get p2p chat info

```
get_p2p_chat_info(mid, from_uid, to_uid, callback = None, timeout = 0)
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### get_group_chat_info

##### get group chat info

```
get_group_chat_info(mid, from_uid, gid, callback = None, timeout = 0)
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### get_room_chat_info

##### get room chat info

```
get_room_chat_info(mid, from_uid, rid, callback = None, timeout = 0)
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### get_broadcast_chat_info

##### get broadcast chat info

```
get_broadcast_chat_info(self, mid, from_uid, callback = None, timeout = 0)
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
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### translate

##### translate api

```
translate(text, dst, src = None, ttype = 'chat', profanity = 'off', post_profanity = False, uid = None, callback = None, timeout = 0)
```

#### params:

* text: **(Required | str)**  text to translate
* dst: **(Required | str)**  target language type
* src: **(Optional | str)**  source language typ
* ttype: **(Optional | str)**  'chat' or 'mail'
* profanity: **(Optional | str)**  sensitive language filtering 'off', 'stop' or 'censor'
* post_profanity: **(Optional | bool)**  whether to filter the translated text
* uid: **(Optional | int)**  user id
* callback: **(Optional | a sub-class of TranslateCallback )**  used in async implementation

```python
class TranslateCallback(object):
    def callback(self, result, error_code):
        pass
      
# result is:
class TranslateResult(object):
    def __init__(self):
        self.source = str()
        self.target = str()
        self.source_text = str()
        self.target_text = str()
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(TranslateResult)** translate result
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 



### text check

##### text check api

```
text_check(text, uid = None, callback = None, timeout = 0)
```

#### params:

* text: **(Required | str)**  text to check
* uid: **(Optional | int)**  user id
* callback: **(Optional | a sub-class of ProfanityCallback )**  used in async implementation

```python
class TextCheckCallback(object):
    def callback(self, result, error_code):
        pass
      
# result is:
class TextCheckResult(CheckResult):
    def __init__(self):
        CheckResult.__init__(self)
        self.text = str()
        self.wlist = []

# CheckResult is:       
class CheckResult(object):
    def __init__(self):
        self.result = 0
        self.tags = []
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(TextCheckResult)** text check result
    * result.tags: **(list<int>)** Triggered categories, such as pornography and politics, etc., see text review category for details
    * result.wlist: **(list<str>)**  Sensitive word list
    * result.text: **(str)**  The text content after the sensitive word filtering, the sensitive words contained in it will be replaced with *
    * result.result: **(int)**  0: pass，2，not pass
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 


### image check

##### image check api

```
image_check(image, image_type, uid = None, callback = None, timeout = 0)
```

#### params:

* image: **(Required | str)**  image url or content
* image_type: **(Required | int)**  1, url, 2, content
* uid: **(Optional | int)**  user id
* callback: **(Optional | a sub-class of ProfanityCallback )**  used in async implementation

```python
class CheckCallback(object):
    def callback(self, result, error_code):
        pass
      
# result is:  
class CheckResult(object):
    def __init__(self):
        self.result = 0
        self.tags = []
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(TextCheckResult)** text check result
    * result.tags: **(list<int>)** Triggered categories, such as pornography and politics, etc., see text review category for details
    * result.result: **(int)**  0: pass，2，not pass
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 


### audio check

##### audio check api

```
audio_check(audio, audio_type, lang, codec = None, srate = None, uid = None, callback = None, timeout = 0)
```

#### params:

* audio: **(Required | str)**  audio url or content
* audio_type: **(Required | int)**  1, url, 2, content
* lang: **(Required | str)**  language
* codec: **(Optional | str)**  codec default is AMR_WB
* srate: **(Optional | int)**  srate default is 16000
* uid: **(Optional | int)**  user id
* callback: **(Optional | a sub-class of CheckCallback )**  used in async implementation

```python
class CheckCallback(object):
    def callback(self, result, error_code):
        pass
      
# result is:  
class CheckResult(object):
    def __init__(self):
        self.result = 0
        self.tags = []
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(TextCheckResult)** text check result
    * result.tags: **(list<int>)** Triggered categories, such as pornography and politics, etc., see text review category for details
    * result.result: **(int)**  0: pass，2，not pass
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 


### video check

##### video check api

```
video_check(video, video_type, video_name, uid = None, callback = None, timeout = 0)
```

#### params:

* video: **(Required | str)**  video url or content
* video_type: **(Required | int)**  1, url, 2, content
* video_name: **(Required | str)**  video name
* uid: **(Optional | int)**  user id
* callback: **(Optional | a sub-class of CheckCallback )**  used in async implementation

```python
class CheckCallback(object):
    def callback(self, result, error_code):
        pass
      
# result is:  
class CheckResult(object):
    def __init__(self):
        self.result = 0
        self.tags = []
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(TextCheckResult)** text check result
    * result.tags: **(list<int>)** Triggered categories, such as pornography and politics, etc., see text review category for details
    * result.result: **(int)**  0: pass，2，not pass
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 


### speech to text check

##### speech to text check api

```
speech_to_text(audio, audio_type, lang, codec = None, srate = None, uid = None, callback = None, timeout = 0)
```

#### params:

* audio: **(Required | str)**  audio url or content
* audio_type: **(Required | int)**  1, url, 2, content
* lang: **(Required | str)**  language
* codec: **(Optional | str)**  codec default is AMR_WB
* srate: **(Optional | int)**  srate default is 16000
* uid: **(Optional | int)**  user id
* callback: **(Optional | a sub-class of CheckCallback )**  used in async implementation

```python
class SpeechToTextCallback(object):
    def callback(self, result, error_code):
        pass
      
# result is:  
class SpeechToTextResult(object):
    def __init__(self):
        self.text = str()
        self.lang = str()
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(TextCheckResult)** text check result
    * result.text: **(str)** text
    * result.lang: **(str)**  language
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when 
