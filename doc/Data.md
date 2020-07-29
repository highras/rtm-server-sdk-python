# RTM Server-End Python SDK Data API Docs

# Index

[TOC]

## API

### data_set

##### set data

```
data_set(uid, key, value, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* key: **(Required | str)**  data key
* value: **(Required | str)** data value
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



### data_delete

##### delete data

```
data_delete(uid, key, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* key: **(Required | str)**  data key
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



### data_get

##### get data

```
data_get(uid, key, callback = None, timeout = 0)
```

#### params:

* uid: **(Required | int)**  user id
* key: **(Required | str)**  data key
* callback: **(Optional | a sub-class of DataGetCallback )**  used in async implementation

```python
class DataGetCallback(object):
    def callback(self, value, error_code):
        pass
```

#### return:

* in async implementation, return None

* in sync implementation:

  * value:  **(str)** data value
  * error_code:  **(int)**   the error code when quest is fail, or FPNN_ERROR.FPNN_EC_OK when success

  



