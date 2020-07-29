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
    def callback(self, token, error_code):
        pass
```

#### return:

* in async implementation, return None
* in sync implementation:
  * token:  **(str)** the login token when quest is successful, or None when failed
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success



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
    def callback(self, error_code):
        pass
```

#### return:

* in async implementation, return None

* in sync implementation:

  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success

  

