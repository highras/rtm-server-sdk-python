#encoding=utf8

RTM_SDK_VERSION = '2.2.0'
RTM_INTERFACE_VERSION = '2.6.1'

class RTMServerConfig(object):
    GLOBAL_CONNECT_TIMEOUT_SECONDS = 30
    GLOBAL_QUEST_TIMEOUT_SECONDS = 30
    FILE_GATE_CLIENT_HOLDING_SECONDS = 150
    ERROR_RECORDER = None

    def __init__(self):
        self.global_connect_timeout = RTMServerConfig.GLOBAL_CONNECT_TIMEOUT_SECONDS
        self.global_quest_timeout = RTMServerConfig.GLOBAL_QUEST_TIMEOUT_SECONDS
        self.file_client_holding_seconds = RTMServerConfig.FILE_GATE_CLIENT_HOLDING_SECONDS
        self.error_recorder = RTMServerConfig.ERROR_RECORDER

    @classmethod
    def config(self, conf):
        RTMServerConfig.GLOBAL_CONNECT_TIMEOUT_SECONDS = conf.global_connect_timeout
        RTMServerConfig.GLOBAL_QUEST_TIMEOUT_SECONDS = conf.global_quest_timeout
        RTMServerConfig.FILE_GATE_CLIENT_HOLDING_SECONDS = conf.file_client_holding_seconds
        RTMServerConfig.ERROR_RECORDER = conf.error_recorder

class RTMServerConfigCenter(object):
    @classmethod
    def init(self, conf = None):
        if conf != None:
            RTMServerConfig.config(conf)


