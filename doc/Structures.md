# RTM Server-End Python SDK API Docs: Structures

# Index

[TOC]

### AudioInfo

```
class AudioInfo(object):
    def __init__(self):
        self.source_language = ""
        self.recognized_language = ""
        self.recognized_text = ""
        self.duration = 0
```

### TranslatedInfo

```
class TranslatedInfo(object):
    def __init__(self):
        self.source_language = ""
        self.target_language = ""
        self.source_text = ""
        self.target_text = ""
```

### RTMMessage

```
class RTMMessage(object):
    def __init__(self):
        self.from_uid = 0
        self.to_id = 0
        self.message_type = 0
        self.message_id = 0
        self.message = None
        self.attrs = None
        self.modified_time = 0
        self.audio_info = None
```

* When `message_type == ChatMessageType.AUDIO`, `audio_info` will be assigned, and the `message` may be the recognized message, or empty string;  
* When `message_type` is a kinds of File types, `message` will be assigned the stored address.  

### RetrievedMessage

```
class RetrievedMessage(object):
    def __init__(self):
        self.cursor_id = 0
        self.message_type = 0
        self.message = None
        self.attrs = None
        self.modified_time = 0
```

### HistoryMessage

```
class HistoryMessage(RTMMessage):
    def __init__(self):
        self.cursor_id = 0
```

* Using for history message result.

* The fields are same as the `class RTMMessage`.

### HistoryMessageResult

```
class HistoryMessageResult(object):
    def __init__(self):
        self.count = 0
        self.last_cursor_id = 0
        self.begin_msec = 0
        self.end_msec = 0
        self.messages = []
```

* HistoryMessageResult.messages is a list of `HistoryMessage`
* Using as the result of history message & chat methods.

* When calling history message or history chat methods for fetching subsequent message or chat data, please using the corresponding fields in the result.