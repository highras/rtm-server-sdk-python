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
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success

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
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success



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
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success

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
    def callback(self, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error:  **(QuestError)**   the error when quest is fail, or None when success

#### NOTE:

##### full coverage, only valid for the current connection



## Set Monitor Processor

#### if use the listen* api, you can set the monitor processor to handle the server-end push like this:

```python
class MyRTMQuestProcessor(RTMQuestProcessor):
      def __init__(self):
          pass

      def ping(self):
          print("ping")

      def push_message(self, from_uid, to_uid, mtype, mid, msg, attrs, mtime):
          print("push_message: ", from_uid, to_uid, mtype, mid, msg, attrs, mtime)

      def push_group_message(self, from_uid, gid, mtype, mid, msg, attrs, mtime):
          print("push_group_message: ", from_uid, gid, mtype, mid, msg, attrs, mtime)

      def push_room_message(self, from_uid, rid, mtype, mid, msg, attrs, mtime):
          print("push_room_message: ", from_uid, rid, mtype, mid, msg, attrs, mtime)

      def push_event(self, pid, event, uid, time, endpoint, data):
          print("event: ", pid, event, uid, time, endpoint, data)

      def push_file(self, from_uid, to_uid, mtype, mid, msg, attrs, mtime):
          print("push_file: ", from_uid, to_uid, mtype, mid, msg, attrs, mtime)

      def push_group_file(self, from_uid, gid, mtype, mid, msg, attrs, mtime):
          print("push_group_file: ", from_uid, gid, mtype, mid, msg, attrs, mtime)

      def push_room_file(self, from_uid, rid, mtype, mid, msg, attrs, mtime):
          print("push_room_file: ", from_uid, rid, mtype, mid, msg, attrs, mtime)

      def push_chat(self, from_uid, to_uid, mid, msg, attrs, mtime):
          print("push_chat: ", from_uid, to_uid, mid, msg, attrs, mtime)

      def push_group_chat(self, from_uid, gid, mid, msg, attrs, mtime):
          print("push_group_chat: ", from_uid, gid, mid, msg, attrs, mtime)

      def push_room_chat(self, from_uid, rid, mid, msg, attrs, mtime):
          print("push_room_chat: ", from_uid, rid, mid, msg, attrs, mtime)

      def push_audio(self, from_uid, to_uid, mid, msg, attrs, mtime):
          print("push_audio: ", from_uid, to_uid, mid, msg, attrs, mtime)

      def push_group_audio(self, from_uid, gid, mid, msg, attrs, mtime):
          print("push_group_audio: ", from_uid, gid, mid, msg, attrs, mtime)

      def push_room_audio(self, from_uid, rid, mid, msg, attrs, mtime):
          print("push_room_audio: ", from_uid, rid, mid, msg, attrs, mtime)

      def push_cmd(self, from_uid, to_uid, mid, msg, attrs, mtime):
          print("push_cmd: ", from_uid, to_uid, mid, msg, attrs, mtime)

      def push_group_cmd(self, from_uid, gid, mid, msg, attrs, mtime):
          print("push_group_cmd: ", from_uid, gid, mid, msg, attrs, mtime)

      def push_room_cmd(self, from_uid, rid, mid, msg, attrs, mtime):
          print("push_room_cmd: ", from_uid, rid, mid, msg, attrs, mtime)

client.set_quest_processor(MyRTMQuestProcessor())
```

