# RTM Server-End Python SDK RTC API Docs

# Index

[TOC]

## API

### invite_user_into_voice_room

##### invite user into voice room

```
invite_user_into_voice_room(room_id, to_uids, from_uid, callback = None, timeout = 0):
```

#### params:

* room_id: **(Required | int)**  room id
* to_uids: **(Required | [int64])**  uid of the invited users
* from_uid: **(Required | [int64])**  uid of the inviter
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



### close_voice_room

##### close voice room

```
close_voice_room(self, room_id, callback = None, timeout = 0):
```

#### params:

* room_id: **(Required | int)**  room id
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



### kick_out_from_voice_room

##### kick out user from the voice room

```
kick_out_from_voice_room(uid, room_id, from_uid, callback = None, timeout = 0):
```

#### params:

* uid: **(Required | int64)**  uid of the kicked user
* room_id: **(Required | int)**  room id
* from_uid: **(Required | [int64])**  uid of the kicker
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



### get_voice_room_list

##### get list of the voice rooms

```
get_voice_room_list(callback = None, timeout = 0):
```

#### params:

* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class GetVoiceRoomListCallback(object):
    def callback(self, result, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_voice_room_members

##### get members of the voice room

```
get_voice_room_members(room_id, callback = None, timeout = 0):
```

#### params:

* room_id: **(Required | int)**  room id
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class GetVoiceRoomMembersCallback(object):
    def callback(self, result, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### get_voice_room_member_count

##### get member count of the voice room

```
get_voice_room_member_count(room_id, callback = None, timeout = 0):
```

#### params:

* room_id: **(Required | int)**  room id
* callback: **(Optional | a sub-class of BasicCallback )**  used in async implementation

```python
class GetVoiceRoomMemberCountCallback(object):
    def callback(self, result, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



### set_voice_room_mic_status

##### set the default microphone status of the voice room

```
set_voice_room_mic_status(room_id, status, callback = None, timeout = 0):
```

#### params:

* room_id: **(Required | int)**  room id
* status: **(Required | bool)**  default microphone status, false for close, true for open
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



### pull_into_voice_room

##### pull user into the voice room

```
pull_into_voice_room(room_id, to_uids, callback = None, timeout = 0):
```

#### params:

* room_id: **(Required | int)**  room id
* to_uids: **(Required | [int64])**  list to the pulled uids
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

