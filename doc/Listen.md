# RTM Server-End Python SDK Listen & Monitor API Docs

# Index

[TOC]

## API

### add_listen

##### add server listen to some message or events

```
add_listen(gids = None, rids = None, uids = None, events = None, callback = None, timeout = 0)
```

#### params:

* gids: **(Optional | [int])**  if exist, will listen the group message from the gids
* rids: **(Optional | [int])**  if exist, will listen the room message from the rids
* uids: **(Optional | [int])**  if exist, will listen the P2P message from the uids
* events: **(Optional | [str])**  if exist, will listen the events, event name support [login, logout] now
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

#### NOTE:

##### add incrementally, only valid for the current connection



### remove_listen

##### add server listen to some message or events

```
remove_listen(gids = None, rids = None, uids = None, events = None, callback = None, timeout = 0)
```

#### params:

* gids: **(Optional | [int])**  if exist, will remove listen the group message from the gids
* rids: **(Optional | [int])**  if exist, will remove listen the room message from the rids
* uids: **(Optional | [int])**  if exist, will remove listen the P2P message from the uids
* events: **(Optional | [str])**  if exist, will remove listen the events, event name support [login, logout] now
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



### set_listen

##### set server listen to some message or events

```
set_listen(gids = None, rids = None, uids = None, events = None, callback = None, timeout = 0)
```

#### params:

* gids: **(Optional | [int])**  if exist, will listen the group message from the gids
* rids: **(Optional | [int])**  if exist, will listen the room message from the rids
* uids: **(Optional | [int])**  if exist, will listen the P2P message from the uids
* events: **(Optional | [str])**  if exist, will listen the events, event name support [login, logout] now
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

#### NOTE:

##### full coverage, only valid for the current connection



### set_all_listen

##### set server listen to all message or events

```
set_all_listen(p2p = None, group = None, room = None, ev = None, callback = None, timeout = 0)
```

#### params:

* p2p: **(Optional | bool)**  if exist, will listen all the p2p message
* group: **(Optional | bool)**  if exist, will listen all the group message
* room: **(Optional | bool)**  if exist, will listen all the room message
* ev: **(Optional | bool)**  if exist, will listen all the events
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

#### NOTE:

##### full coverage, only valid for the current connection



## Set Monitor Processor

#### If use the listen* api, you can set the monitor processor to handle the server-end push like this:

#### Each push method, message param is RTMMessage. Please refer [RTM Structures](Structures.md#RTMMessage).

```python
class MyRTMQuestProcessor(RTMServerPushMonitor):
    def __init__(self):
        pass

    def print_messagee(messag):
        print("from_uid: ", messag.from_uid)
        print("to_id: ", messag.to_id)
        print("message_type: ", message.message_type)
        print("message_id: ", message.message_id)
        print("message: ", message.message)
        print("attrs: ", message.attrs)
        print("modified_time: ", message.modified_time)
        if message.audio_info != None:
            print("audio_info.source_language: ", message.audio_info.source_language)
            print("audio_info.recognized_language: ", message.audio_info.recognized_language)
            print("audio_info.recognized_text: ", message.audio_info.recognized_text)
            print("audio_info.duration: ", message.audio_info.duration)
        if message.translated_info != None:
            print("translated_info.source_language", message.translated_info.source_language)
            print("translated_info.target_language", message.translated_info.target_language)
            print("translated_info.source_text", message.translated_info.source_text)
            print("translated_info.target_text", message.translated_info.target_text)

    def ping(self):
        print("ping")

    def push_message(self, message):
        self.print_message(message)

    def push_group_message(self, message):
        self.print_message(message)

    def push_room_message(self, message):
        self.print_message(message)

    def push_event(self, pid, event, uid, time, endpoint, data):
        self.print_message(message)

    def push_file(self, message):
        self.print_message(message)

    def push_group_file(self, message):
        self.print_message(message)

    def push_room_file(self, message):
        self.print_message(message)

    def push_chat(self, message):
        self.print_message(message)

    def push_group_chat(self, message):
        self.print_message(message)

    def push_room_chat(self, message):
        self.print_message(message)

    def push_audio(self, message):
        self.print_message(message)

    def push_group_audio(self, message):
        self.print_message(message)

    def push_room_audio(self, message):
        self.print_message(message)

    def push_cmd(self, message):
        self.print_message(message)

    def push_group_cmd(self, message):
        self.print_message(message)

    def push_room_cmd(self, message):
        self.print_message(message)

client.set_quest_processor(MyRTMQuestProcessor())
```

