# RTM Server-End Python SDK Token API Docs

# Index

[TOC]

## API

### get_token

##### get user login token

```
get_token(uid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  the user id
* callback: **(Optional | a sub-class of GetTokenCallback )**  used in async implementation

```python
class GetTokenCallback(object):
    def callback(self, token, error):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * token:  **(str)** the login token when quest is successful, or None when failed
  * error:  **(QuestError)**   the error when quest is fail, or None when success



### remove_token

##### remove a user login token

```
remove_token(uid, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  the user id
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

  

