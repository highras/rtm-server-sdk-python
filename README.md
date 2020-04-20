# RTM Server-End Python SDK

[TOC]

## Depends

* Python 3+
* selectors
* msgpack
* cryptography



## Use

```python
import sys
sys.path.append("/path/to/rtm")
from rtm import *
```



## Notice

**Before using the SDK, please make sure the server time is correct, RTM-Server will check whether the signature time has expired**



## Usage

### Create RTMClient

```python
client = RTMServerClient(pid, secret, endpoint, auto_reconnect, quest_timeout_milliseconds)
```

* please get your project params from RTM Console.
* **auto_reconnect** means establishing the connection in implicit or explicit. NOT keep the connection.



### Configure (Optional)

#### set_quest_timeout

```python
client.set_quest_timeout(timeout)
```

* timeout is in **milliseconds**, this api can set the global quest timeout, you can also set a timeout for each request individually



#### set_connection_callback

```python
client.set_connection_callback(callback)
```

* the callback is a sub-class of ConnectionCallback, you can use it like this:

```python
class MyConnectionCallback(ConnectionCallback):
    def connected(self, connection_id, endpoint):
        print("connected")
        print(connection_id)
        print(endpoint)

    def closed(self, connection_id, endpoint, caused_by_error):
        print("closed")
        print(connection_id)
        print(endpoint)
        print(caused_by_error)

client.set_connection_callback(MyConnectionCallback())
```



#### enable_encryptor_by_pem_file

```python
client.enable_encryptor_by_pem_file(pem_pub_file, curve_name, strength)
```

* RTM Server-End Python SDK using **ECC**/**ECDH** to exchange the secret key, and using **AES-128** or **AES-256** in **CFB** mode to encrypt the whole session in **stream** way.



#### set_quest_processor

```python
client.set_quest_processor(processor)
```

* set the server quest processor to get the event and message forward from the RTM-Server, you can see the detailed usage in the Listening section below



## API

### common params

* each api has two common params: callback and timeout
* timeout is the quest timeout in  **milliseconds**

* each api has both synchronous and asynchronous implementation depends on the parameter callback：

```python
# a get_token example in sync:
token, error = client.get_token(uid)
if error == None:
    print("[Sync get_token ok] : token = " + token)
else:
    print("[Sync get_token error] : " + str(error))
    
# a get_token example in async:
class MyGetTokenCallback(GetTokenCallback):
    def callback(self, token, error):
        if error == None:
            print("[Async get_token ok] : token = " + token)
        else:
            print("[Async get_token error] : code : " + str(error.code) + " message: " + error.message)
client.get_token(uid, callback = MyGetTokenCallback())
```

* the document will introduce the return parameter type and callback function type of each api



### Token Functions

Please refer to 

[Token.md](doc/Token.md)



### Chat Functions

Please refer to 

[Chat.md](doc/Chat.md)



### Message Functions

Please refer to 

[Message.md](doc/Message.md)



### Files Functions

Please refer to 

[Files.md](doc/Files.md)



### Friend Functions

Please refer to 

[Friend.md](doc/Friend.md)



### Group Functions

Please refer to 

[Group.md](doc/Group.md)



### Room Functions

Please refer to 

[Room.md](doc/Room.md)



### User Functions

Please refer to 

[User.md](doc/User.md)



### Data Functions

Please refer to 

[Data.md](doc/Data.md)



### Device Functions

Please refer to 

[Device.md](doc/Device.md)



### Listen & Monitor Functions

Please refer to 

[Listen.md](doc/Listen.md)





