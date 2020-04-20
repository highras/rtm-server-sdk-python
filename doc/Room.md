# RTM Server-End Python SDK Room API Docs

# Index

[TOC]

## API

### add_room_member

##### add room member

```
add_room_member(rid, uid, callback = None, timeout = 0)
```

#### params:

* rid: **(Required | int)**  room id
* uid: **(Optional | int)**  user id
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



### delete_room_member

##### delete room member

```
delete_room_member(rid, uid, callback = None, timeout = 0)
```

#### params:

* rid: **(Required | int)**  room id
* uid: **(Optional | int)**  user id
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



### set_room_info

##### set room public and private info

```
set_room_info(rid, oinfo = None, pinfo = None, callback = None, timeout = 0)
```

#### params:

* rid: **(Required | int)**  room id
* oinfo: **(Optional | str)**  public info
* pinfo: **(Optional | str)**  private info
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



### get_room_info

##### get room public and private info

```
get_room_info(rid, callback = None, timeout = 0)
```

#### params:

* rid: **(Required | int)**  room id
* callback: **(Optional | a sub-class of GetRoomInfoCallback )**  used in async implementation

```python
class GetRoomInfoCallback(object):
    def callback(self, oinfo, pinfo, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * oinfo:  **(int)** public info
  * pinfo:  **(int)** private info
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### add_room_ban

##### add room ban

```
add_room_ban(rid, uid, btime, callback = None, timeout = 0)
```

#### params:

* rid: **(Required | int)**  room id
* uid: **(Required | int)**  user id
* btime: **(Optional | int)**  ban time in second
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



### remove_room_ban

##### remove room ban

```
remove_room_ban(rid, uid, callback = None, timeout = 0)
```

#### params:

* rid: **(Required | int)**  room id
* uid: **(Required | int)**  user id
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



### is_ban_of_room

##### check is ban of a room

```
is_ban_of_room(rid, uid, callback = None, timeout = 0)
```

#### params:

* rid: **(Required | int)**  room id
* uid: **(Required | int)**  user id
* callback: **(Optional | a sub-class of IsBanOfRoomCallback )**  used in async implementation

```python
class IsBanOfRoomCallback(object):
    def callback(self, ok, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * ok:  **(bool)** is ban
  * error:  **(QuestError)**   the error when quest is fail, or None when success



