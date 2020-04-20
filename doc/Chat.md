# RTM Server-End Python SDK Chat API Docs

# Index

[TOC]

## API

### send_chat

##### send a P2P chat

```
send_chat(from_uid, to_uid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* to_uid: **(Required | int)**  to user id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success

#### **NOTICE:**

* in send_chat/send_chats/send_group_chat/send_room_chat/broadcast_chat, if you turn on automatic translation in value-added services, the msg params must be the original chat text



### send_chats

##### send a muti-user chat

```
send_chats(from_uid, to_uids, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* to_uids: **(Required | [int])**  to user id list
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_group_chat

##### send a group chat

```
send_group_chat(from_uid, gid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* gid: **(Required | int)**  group id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_room_chat

##### send a room chat

```
send_room_chat(from_uid, rid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* rid: **(Required | int)**  room id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### broadcast_chat

##### broadcast chat

```
broadcast_chat(from_uid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_audio

##### send a P2P audio

```
send_audio(from_uid, to_uid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* to_uid: **(Required | int)**  to user id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_audios

##### send a muti-user audio

```
send_audios(from_uid, to_uids, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* to_uids: **(Required | [int])**  to user id list
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_group_audio

##### send a group audio

```
send_group_audio(from_uid, gid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* gid: **(Required | int)**  group id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_room_audio

##### send a room audio

```
send_room_audio(from_uid, rid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* rid: **(Required | int)**  room id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### broadcast_audio

##### broadcast audio

```
broadcast_audio(from_uid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_cmd

##### send a P2P cmd

```
send_cmd(from_uid, to_uid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* to_uid: **(Required | int)**  to user id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_cmds

##### send a muti-user cmd

```
send_cmds(from_uid, to_uids, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* to_uids: **(Required | [int])**  to user id list
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_group_cmd

##### send a group cmd

```
send_group_cmd(from_uid, gid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* gid: **(Required | int)**  group id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### send_room_cmd

##### send a room cmd

```
send_room_cmd(from_uid, rid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* rid: **(Required | int)**  room id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### broadcast_cmd

##### broadcast cmd

```
broadcast_cmd(from_uid, msg, attrs, mid = 0, callback = None, timeout = 0)
```

#### params:

* from_uid: **(Required | int)**  from user id
* msg: **(Required | str)**  message content
* attrs: **(Required | str)**  message attributes
* mid: **(Optional | int)**  message id, if mid = 0, will generate a new mid
* callback: **(Optional | a sub-class of SendMessageCallback )**  used in async implementation

```python
class SendMessageCallback(object):
    def callback(self, mid, mtime, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * mid:  **(int)** message id
  * mtime:  **(int)** server returned timestamp in seconds
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, result, error):
        pass

# result is:
class GetGroupMessageResult(object):
    def __init__(self):
        self.num = 0
        self.lastid = 0
        self.begin = 0
        self.end = 0
        self.msgs = []
        
# GetGroupMessageResult.msgs is list of:
class GroupMessage(object):
    def __init__(self):
        self.id = 0
        self.from_uid = 0
        self.mtype = 0
        self.mid = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(GetGroupMessageResult)** message result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, result, error):
        pass

# result is:
class GetRoomMessageResult(object):
    def __init__(self):
        self.num = 0
        self.lastid = 0
        self.begin = 0
        self.end = 0
        self.msgs = []
        
# GetRoomMessageResult.msgs is list of:
class RoomMessage(object):
    def __init__(self):
        self.id = 0
        self.from_uid = 0
        self.mtype = 0
        self.mid = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(GetRoomMessageResult)** message result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, result, error):
        pass

# result is:
class GetBroadcastMessageResult(object):
    def __init__(self):
        self.num = 0
        self.lastid = 0
        self.begin = 0
        self.end = 0
        self.msgs = []
        
# GetBroadcastMessageResult.msgs is list of:
class BroadcastMessage(object):
    def __init__(self):
        self.id = 0
        self.from_uid = 0
        self.mtype = 0
        self.mid = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(GetBroadcastMessageResult)** message result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, result, error):
        pass

# result is:
class GetP2PMessageResult(object):
    def __init__(self):
        self.num = 0
        self.lastid = 0
        self.begin = 0
        self.end = 0
        self.msgs = []
        
# GetBroadcastMessageResult.msgs is list of:
class P2PMessage(object):
    def __init__(self):
        self.id = 0
        self.direction = 0
        self.mtype = 0
        self.mid = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(GetP2PMessageResult)** message result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, result, error):
        pass
      
# result is:
class MessageInfoResult(object):
    def __init__(self):
        self.id = 0
        self.mtype = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(MessageInfoResult)** message result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, result, error):
        pass
      
# result is:
class MessageInfoResult(object):
    def __init__(self):
        self.id = 0
        self.mtype = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(MessageInfoResult)** message result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, result, error):
        pass
      
# result is:
class MessageInfoResult(object):
    def __init__(self):
        self.id = 0
        self.mtype = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(MessageInfoResult)** message result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, result, error):
        pass
      
# result is:
class MessageInfoResult(object):
    def __init__(self):
        self.id = 0
        self.mtype = 0
        self.msg = str()
        self.attrs = str()
        self.mtime = 0
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(MessageInfoResult)** message result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, result, error):
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
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### profanity

##### profanity api

```
profanity(text, classify = False, uid = None, callback = None, timeout = 0)
```

#### params:

* text: **(Required | str)**  text to profanity
* classify: **(Optional | bool)**  whether to perform text classification detection
* uid: **(Optional | int)**  user id
* callback: **(Optional | a sub-class of ProfanityCallback )**  used in async implementation

```python
class ProfanityCallback(object):
    def callback(self, result, error):
        pass
      
# result is:
class ProfanityResult(object):
    def __init__(self):
        self.text = str()
        self.classification = []
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(ProfanityResult)** profanity result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### transcribe

##### transcribe api

```
transcribe(audio, uid = None, profanity_filter = False, callback = None, timeout = 0)
```

#### params:

* audio: **(Required | bytes)**  audio binary bytes
* profanity_filter: **(Optional | bool)**  profanity the result
* uid: **(Optional | int)**  user id
* callback: **(Optional | a sub-class of TranscribeCallback )**  used in async implementation

```python
class TranscribeCallback(object):
    def callback(self, result, error):
        pass
      
# result is:
class TranscribeResult(object):
    def __init__(self):
        self.text = str()
        self.lang = str()
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(TranscribeResult)** transcribe result
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### profanity

##### profanity api

```
profanity(text, classify = False, uid = None, callback = None, timeout = 0)
```

#### params:

* text: **(Required | str)**  text to profanity
* classify: **(Optional | bool)**  whether to perform text classification detection
* uid: **(Optional | int)**  user id
* callback: **(Optional | a sub-class of ProfanityCallback )**  used in async implementation

```python
class ProfanityCallback(object):
    def callback(self, result, error):
        pass
      
# result is:
class ProfanityResult(object):
    def __init__(self):
        self.text = str()
        self.classification = []
```

#### return:

* in async implementation, return None
* in sync implementation:
  * result:  **(ProfanityResult)** profanity result
  * error:  **(QuestError)**   the error when quest is fail, or None when success

