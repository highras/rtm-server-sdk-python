#encoding=utf8
import sys
sys.path.append("../src")
import time
from rtm import *

def test_token_and_system(client):
    token, error_code = client.get_token(12345)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_token ok] : token = " + token)
    else:
        print("[Sync get_token error_code] : " + str(error_code))

    class MyGetTokenCallback(GetTokenCallback):
        def callback(self, token, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_token ok] : token = " + token)
            else:
                print("[Async get_token error_code] : " + str(error_code))
    client.get_token(12345, callback = MyGetTokenCallback())

    error_code = client.kickout(12345)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync kickout ok]")
    else:
        print("[Sync kickout error_code] : " + str(error_code))

    class MyKickoutCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async kickout ok]")
            else:
                print("[Async kickout error_code] : " + str(error_code))
    client.kickout(12345, callback = MyKickoutCallback())

    error_code = client.add_device(12345, 'apns', 'xxxxxxx')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync add_device ok]")
    else:
        print("[Sync add_device error_code] : " + str(error_code))

    class MyAddDeviceCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async add_device ok]")
            else:
                print("[Async add_device error_code] : " + str(error_code))
    client.add_device(12345, 'apns', 'xxxxxxx', callback = MyAddDeviceCallback())

    error_code = client.remove_device(12345, 'xxxxxxx')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync remove_device ok]")
    else:
        print("[Sync remove_device error_code] : " + str(error_code))

    class MyRemoveDeviceCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async remove_device ok]")
            else:
                print("[Async remove_device error_code] : " + str(error_code))
    client.remove_device(12345, 'xxxxxxx', callback = MyRemoveDeviceCallback())

    error_code = client.remove_token(12345)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync remove_token ok]")
    else:
        print("[Sync remove_token error_code] : " + str(error_code))

    class MyRemoveTokenCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async remove_token ok]")
            else:
                print("[Async remove_token error_code] : " + str(error_code))
    client.remove_token(12345, callback = MyRemoveTokenCallback())
    
def test_send_message(client):
    mid, mtime, error_code = client.send_message(51, 123456, 654321, 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync send_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_message error_code] : " + str(error_code))

    class MySendMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async send_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_message error_code] : " + str(error_code))
    client.send_message(51, 123456, 654321, 'test msg', 'test attrs', callback = MySendMessageCallback())

    mid, mtime, error_code = client.send_messages(51, 123456, [654321, 123], 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync send_messages ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_messages error_code] : " + str(error_code))

    class MySendMessagesCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async send_messages ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_messages error_code] : " + str(error_code))
    client.send_messages(51, 123456, [654321, 123], 'test msg', 'test attrs', callback = MySendMessagesCallback())

    mid, mtime, error_code = client.send_group_message(51, 123456, 123, 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync send_group_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_group_message error_code] : " + str(error_code))

    class MySendGroupMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async send_group_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_group_message error_code] : " + str(error_code))
    client.send_group_message(51, 123456, 123, 'test msg', 'test attrs', callback = MySendGroupMessageCallback())

    mid, mtime, error_code = client.send_room_message(51, 123456, 123, 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync send_room_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_room_message error_code] : " + str(error_code))

    class MySendRoomMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async send_room_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_room_message error_code] : " + str(error_code))
    client.send_room_message(51, 123456, 123, 'test msg', 'test attrs', callback = MySendRoomMessageCallback())

    mid, mtime, error_code = client.broadcast_message(51, 111, 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync broadcast_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync broadcast_message error_code] : " + str(error_code))

    class MyBroadcastMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async broadcast_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async broadcast_message error_code] : " + str(error_code))
    client.broadcast_message(51, 111, 'test msg', 'test attrs', callback = MyBroadcastMessageCallback())

def test_get_message(client):
    result, error_code = client.get_group_message(123456, 123, True, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_group_message ok] : count = " + str(result.count))
    else:
        print("[Sync get_group_message error_code] : " + str(error_code))

    class MyGetGroupMessageCallback(GetGroupMessageCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_group_message ok] : count = " + str(result.count))
            else:
                print("[Async get_group_message error_code] : " + str(error_code))
    client.get_group_message(123456, 123, True, 10, callback = MyGetGroupMessageCallback())

    result, error_code = client.get_room_message(123456, 123, True, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_room_message ok] : count = " + str(result.count))
    else:
        print("[Sync get_room_message error_code] : " + str(error_code))

    class MyGetRoomMessageCallback(GetRoomMessageCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_room_message ok] : count = " + str(result.count))
            else:
                print("[Async get_room_message error_code] : " + str(error_code))
    client.get_room_message(123456, 123, True, 10, callback = MyGetRoomMessageCallback())

    result, error_code = client.get_broadcast_message(111, True, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_broadcast_message ok] : count = " + str(result.count))
    else:
        print("[Sync get_broadcast_message error_code] : " + str(error_code))

    class MyGetBroadcastMessageCallback(GetBroadcastMessageCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_broadcast_message ok] : count = " + str(result.count))
            else:
                print("[Async get_broadcast_message error_code] : " + str(error_code))
    client.get_broadcast_message(111, True, 10, callback = MyGetBroadcastMessageCallback())

    result, error_code = client.get_p2p_message(123456, 654321, True, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_p2p_message ok] : count = " + str(result.count))
    else:
        print("[Sync get_p2p_message error_code] : " + str(error_code))

    class MyGetP2PMessageCallback(GetP2PMessageCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_p2p_message ok] : count = " + str(result.count))
            else:
                print("[Async get_p2p_message error_code] : " + str(error_code))
    client.get_p2p_message(123456, 654321, True, 10, callback = MyGetP2PMessageCallback())

def test_delete_message(client):
    error_code = client.delete_p2p_message(1111111, 12345, 654321)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync delete_p2p_message ok]")
    else:
        print("[Sync delete_p2p_message error_code] : " + str(error_code))

    class MyDeleteP2PMessageCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async delete_p2p_message ok]")
            else:
                print("[Async delete_p2p_message error_code] : " + str(error_code))
    client.delete_p2p_message(1111111, 12345, 654321, callback = MyDeleteP2PMessageCallback())

    error_code = client.delete_group_message(1111111, 12345, 123)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync delete_group_message ok]")
    else:
        print("[Sync delete_group_message error_code] : " + str(error_code))

    class MyDeleteGroupMessageCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async delete_group_message ok]")
            else:
                print("[Async delete_group_message error_code] : " + str(error_code))
    client.delete_group_message(1111111, 12345, 123, callback = MyDeleteGroupMessageCallback())

    error_code = client.delete_room_message(1111111, 12345, 123)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync delete_room_message ok]")
    else:
        print("[Sync delete_room_message error_code] : " + str(error_code))

    class MyDeleteRoomMessageCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async delete_room_message ok]")
            else:
                print("[Async delete_room_message error_code] : " + str(error_code))
    client.delete_room_message(1111111, 12345, 123, callback = MyDeleteRoomMessageCallback())

    error_code = client.delete_broadcast_message(1111111, 111)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync delete_broadcast_message ok]")
    else:
        print("[Sync delete_broadcast_message error_code] : " + str(error_code))

    class MyDeleteBroadcastMessageCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async delete_broadcast_message ok]")
            else:
                print("[Async delete_broadcast_message error_code] : " + str(error_code))
    client.delete_broadcast_message(1111111, 111, callback = MyDeleteBroadcastMessageCallback())

def test_get_message_info(client):
    result, error_code = client.get_p2p_message_info(1111111, 123456, 654321)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_group_message ok] : message = " + str(result.message))
    else:
        print("[Sync get_group_message error_code] : " + str(error_code))

    class MyGetP2PMessageInfoCallback(GetMessageInfoCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Sync get_group_message ok] : message = " + str(result.message))
            else:
                print("[Sync get_group_message error_code] : " + str(error_code))
    client.get_p2p_message_info(1111111, 123456, 654321, callback = MyGetP2PMessageInfoCallback())

    result, error_code = client.get_group_message_info(1111111, 123456, 123)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_group_message_info ok] : message = " + str(result.message))
    else:
        print("[Sync get_group_message_info error_code] : " + str(error_code))

    class MyGetGroupMessageInfoCallback(GetMessageInfoCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Sync get_group_message_info ok] : message = " + str(result.message))
            else:
                print("[Sync get_group_message_info error_code] : " + str(error_code))
    client.get_group_message_info(1111111, 123456, 123, callback = MyGetGroupMessageInfoCallback())

    result, error_code = client.get_room_message_info(1111111, 123456, 123)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_room_message_info ok] : message = " + str(result.message))
    else:
        print("[Sync get_room_message_info error_code] : " + str(error_code))

    class MyGetRoomMessageInfoCallback(GetMessageInfoCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Sync get_room_message_info ok] : message = " + str(result.message))
            else:
                print("[Sync get_room_message_info error_code] : " + str(error_code))
    client.get_room_message_info(1111111, 123456, 123, callback = MyGetRoomMessageInfoCallback())

    result, error_code = client.get_broadcast_message_info(1111111, 123456)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_broadcast_message_info ok] : message = " + str(result.message))
    else:
        print("[Sync get_broadcast_message_info error_code] : " + str(error_code))

    class MyGetBroadcastMessageInfoCallback(GetMessageInfoCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Sync get_broadcast_message_info ok] : message = " + str(result.message))
            else:
                print("[Sync get_broadcast_message_info error_code] : " + str(error_code))
    client.get_broadcast_message_info(1111111, 123456, callback = MyGetBroadcastMessageInfoCallback())

def test_send_chat(client):
    mid, mtime, error_code = client.send_chat(123456, 654321, 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync send_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_chat error_code] : " + str(error_code))

    class MySendMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async send_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_chat error_code] : " + str(error_code))
    client.send_chat(123456, 654321, 'test msg', 'test attrs', callback = MySendMessageCallback())

    mid, mtime, error_code = client.send_chats( 123456, [654321, 123], 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync send_chats ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_chats error_code] : " + str(error_code))

    class MySendMessagesCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async send_chats ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_chats error_code] : " + str(error_code))
    client.send_chats(123456, [654321, 123], 'test msg', 'test attrs', callback = MySendMessagesCallback())

    mid, mtime, error_code = client.send_group_chat(123456, 123, 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync send_group_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_group_chat error] : " + str(error_code))

    class MySendGroupMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async send_group_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_group_chat error_code] : " + str(error_code))
    client.send_group_chat(123456, 123, 'test msg', 'test attrs', callback = MySendGroupMessageCallback())

    mid, mtime, error_code = client.send_room_chat(123456, 123, 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync send_room_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_room_chat error_code] : " + str(error_code))

    class MySendRoomMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async send_room_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_room_chat error_code] : " + str(error_code))
    client.send_room_chat(123456, 123, 'test msg', 'test attrs', callback = MySendRoomMessageCallback())

    mid, mtime, error_code = client.broadcast_chat(111, 'test msg', 'test attrs')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync broadcast_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync broadcast_chat error_code] : " + str(error_code))

    class MyBroadcastMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async broadcast_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async broadcast_chat error_code] : " + str(error_code))
    client.broadcast_chat(111, 'test msg', 'test attrs', callback = MyBroadcastMessageCallback())

def test_get_chat(client):
    result, error_code = client.get_group_chat(123456, 123, True, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_group_chat ok] : count = " + str(result.count))
    else:
        print("[Sync get_group_chat error_code] : " + str(error_code))

    class MyGetGroupMessageCallback(GetGroupMessageCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_group_chat ok] : count = " + str(result.count))
            else:
                print("[Async get_group_chat error_code] : " + str(error_code))
    client.get_group_chat(123456, 123, True, 10, callback = MyGetGroupMessageCallback())

    result, error_code = client.get_room_chat(123456, 123, True, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_room_chat ok] : count = " + str(result.count))
    else:
        print("[Sync get_room_chat error_code] : " + str(error_code))

    class MyGetRoomMessageCallback(GetRoomMessageCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_room_chat ok] : count = " + str(result.count))
            else:
                print("[Async get_room_chat error_code] : " + str(error_code))
    client.get_room_chat(123456, 123, True, 10, callback = MyGetRoomMessageCallback())

    result, error_code = client.get_broadcast_chat(111, True, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_broadcast_chat ok] : count = " + str(result.count))
    else:
        print("[Sync get_broadcast_chat error_code] : " + str(error_code))

    class MyGetBroadcastMessageCallback(GetBroadcastMessageCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_broadcast_chat ok] : count = " + str(result.count))
            else:
                print("[Async get_broadcast_chat error_code] : " + str(error_code))
    client.get_broadcast_chat(111, True, 10, callback = MyGetBroadcastMessageCallback())

    result, error_code = client.get_p2p_chat(123456, 654321, True, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_p2p_chat ok] : count = " + str(result.count))
    else:
        print("[Sync get_p2p_chat error_code] : " + str(error_code))

    class MyGetP2PMessageCallback(GetP2PMessageCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_p2p_chat ok] : count = " + str(result.count))
            else:
                print("[Async get_p2p_chat error_code] : " + str(error_code))
    client.get_p2p_chat(123456, 654321, True, 10, callback = MyGetP2PMessageCallback())

def test_translate(client):
    result, error_code = client.translate('hello world', 'zh-CN')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync translate ok] : source = " + result.source + " target = " + result.target + " source_text = " + result.source_text + " target_text = " + result.target_text)
    else:
        print("[Sync translate error_code] : " + str(error_code))

    class MyTranslateCallback(TranslateCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async translate ok] : source = " + result.source + " target = " + result.target + " source_text = " + result.source_text + " target_text = " + result.target_text)
            else:
                print("[Async translate error_code] : " + str(error_code))
    client.translate('hello world', 'zh-CN', callback = MyTranslateCallback())

    result, error_code = client.profanity('出售，海洛因')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync profanity ok] : text = " + result.text + " classification = " + str(result.classification))
    else:
        print("[Sync profanity error_code] : " + str(error_code))

    class MyProfanityCallback(ProfanityCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async profanity ok] : text = " + result.text + " classification = " + str(result.classification))
            else:
                print("[Async profanity error_code] : " + str(error_code))
    client.profanity('出售，海洛因', callback = MyProfanityCallback())

    result, error_code = client.transcribe('a test audio binary')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync transcribe ok] : text = " + result.text + " lang = " + result.lang)
    else:
        print("[Sync transcribe error_code] : " + str(error_code))

    class MyTranscribeCallback(TranscribeCallback):
        def callback(self, result, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async transcribe ok] : text = " + result.text + " lang = " + result.lang)
            else:
                print("[Async transcribe error_code] : " + str(error_code))
    client.transcribe('a test audio binary', callback = MyTranscribeCallback())

def test_file(client):
    token, endpoint, error_code = client.file_token(123, 'sendfile', to_uid = 1234)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync file_token ok] : token = " + token + " endpoint = " + endpoint)
    else:
        print("[Sync file_token error_code] : " + str(error_code))

    class MyFileTokenCallback(FileTokenCallback):
        def callback(self, token, endpoint, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async file_token ok] : token = " + token + " endpoint = " + endpoint)
            else:
                print("[Async file_token error_code] : " + str(error_code))
    client.file_token(123, 'sendfile', to_uid = 1234, callback = MyFileTokenCallback())

    mtime, error_code = client.send_file(123456, 654321, 40, '/Users/zhaojianjun/Downloads/audio1.bin')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync send_file ok] : mtime = " + str(mtime))
    else:
        print("[Sync send_file error_code] : " + str(error_code))
    
    class MySendFileCallback(SendFileCallback):
        def callback(self, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async send_file ok] : mtime = " + str(mtime))
            else:
                print("[Async send_file error_code] : " + str(error_code))
    client.send_file(123456, 654321, 40, '/Users/zhaojianjun/Downloads/audio1.bin', callback = MySendFileCallback(), timeout = 15)

def test_user(client):
    uids, error_code = client.get_online_users([123, 456])
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_online_users ok] : uids = " + str(uids))
    else:
        print("[Sync get_online_users error_code] : " + str(error_code))

    class MyGetOnlineUsersCallback(GetOnlineUsersCallback):
        def callback(self, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_online_users ok] : uids = " + str(uids))
            else:
                print("[Async get_online_users error_code] : " + str(error_code))
    client.get_online_users([123, 456], callback = MyGetOnlineUsersCallback())

    error_code = client.add_project_black(123456789, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync add_project_black ok]")
    else:
        print("[Sync add_project_black error_code] : " + str(error_code))

    class MyAddProjectBlack(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async add_project_black ok]")
            else:
                print("[Async add_project_black error_code] : " + str(error_code))
    client.add_project_black(123456789, 10, callback = MyAddProjectBlack())

    ok, error_code = client.is_project_black(123456789)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync is_project_black ok] ok = " + str(ok))
    else:
        print("[Sync is_project_black error_code] : " + str(error_code))

    class MyIsProjectBlackCallback(IsProjectBlackCallback):
        def callback(self, ok, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async is_project_black ok] ok = " + str(ok))
            else:
                print("[Async is_project_black error_code] : " + str(error_code))
    client.is_project_black(123456789, callback = MyIsProjectBlackCallback())

    error_code = client.set_user_info(123456789, 'test_oinfo', 'test_pinfo')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync set_user_info ok]")
    else:
        print("[Sync set_user_info error_code] : " + str(error_code))

    class MySetUserInfo(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async set_user_info ok]")
            else:
                print("[Async set_user_info error_code] : " + str(error_code))
    client.set_user_info(123456789, 'test_oinfo', 'test_pinfo', MySetUserInfo())

    oinfo, pinfo, error_code = client.get_user_info(123456789)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_user_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
    else:
        print("[Sync get_user_info error_code] : " + str(error_code))

    class MyGetUserInfoCallback(GetUserInfoCallback):
        def callback(self, oinfo, pinfo, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_user_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
            else:
                print("[Async get_user_info error_code] : " + str(error_code))
    client.get_user_info(123456789, callback = MyGetUserInfoCallback())

    info, error_code = client.get_user_open_info([123456789, 123456])
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_user_open_info ok] : info = " + str(info))
    else:
        print("[Sync get_user_open_info error_code] : " + str(error_code))

    class MyGetUserOpenInfoCallback(GetUserOpenInfoCallback):
        def callback(self, info, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_user_open_info ok] : info = " + str(info))
            else:
                print("[Async get_user_open_info error_code] : " + str(error_code))
    client.get_user_open_info([123456789, 123456], callback = MyGetUserOpenInfoCallback())

def test_friend(client):
    error_code = client.add_friends(123456789, [123, 456, 789])
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync add_friends ok]")
    else:
        print("[Sync add_friends error_code] : " + str(error_code))

    class MyAddFriendsCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async add_friends ok]")
            else:
                print("[Async add_friends error_code] : " + str(error_code))
    client.add_friends(123456789, [123, 456, 789], callback = MyAddFriendsCallback())

    error_code = client.delete_friends(123456789, [123])
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync delete_friends ok]")
    else:
        print("[Sync delete_friends error_code] : " + str(error_code))

    class MyDeleteFriendsCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async delete_friends ok]")
            else:
                print("[Async delete_friends error_code] : " + str(error_code))
    client.delete_friends(123456789, [123], callback = MyDeleteFriendsCallback())

    uids, error_code = client.get_friends(123456789)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_friends ok] : uids = " + str(uids))
    else:
        print("[Sync get_friends error_code] : " + str(error_code))

    class MyGetFriendsCallback(GetFriendsCallback):
        def callback(self, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_friends ok] : uids = " + str(uids))
            else:
                print("[Async get_friends error_code] : " + str(error_code))
    client.get_friends(123456789, callback = MyGetFriendsCallback())

    ok, error_code = client.is_friend(123456789, 789)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync is_friend ok] ok = " + str(ok))
    else:
        print("[Sync is_friend error_code] : " + str(error_code))

    class MyIsFriendCallback(IsFriendCallback):
        def callback(self, ok, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async is_friend ok] ok = " + str(ok))
            else:
                print("[Async is_friend error_code] : " + str(error_code))
    client.is_friend(123456789, 789, callback = MyIsFriendCallback())

    fuids, error_code = client.is_friends(123456789, [666, 789])
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync is_friends ok] : fuids = " + str(fuids))
    else:
        print("[Sync is_friends error_code] : " + str(error_code))

    class MyIsFriendsCallback(IsFriendsCallback):
        def callback(self, fuids, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async is_friends ok] : fuids = " + str(fuids))
            else:
                print("[Async is_friends error_code] : " + str(error_code))
    client.is_friends(123456789, [666, 789], callback = MyIsFriendsCallback())

def test_group(client):
    error_code = client.add_group_members(123, [123456789, 666, 888])
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync add_group_members ok]")
    else:
        print("[Sync add_group_members error_code] : " + str(error_code))

    class MyAddGroupMembersCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async add_group_members ok]")
            else:
                print("[Async add_group_members error_code] : " + str(error_code))
    client.add_group_members(123, [123456789, 666, 888], callback = MyAddGroupMembersCallback())

    error_code = client.delete_group_members(123, [123456789, 888])
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync delete_group_members ok]")
    else:
        print("[Sync delete_group_members error_code] : " + str(error_code))

    class MyDeleteGroupMembersCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async delete_group_members ok]")
            else:
                print("[Async delete_group_members error_code] : " + str(error_code))
    client.delete_group_members(123, [123456789, 888], callback = MyDeleteGroupMembersCallback())

    error_code = client.delete_group(1234)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync delete_group ok]")
    else:
        print("[Sync delete_group error_code] : " + str(error_code))

    class MyDeleteGroupCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async delete_group ok]")
            else:
                print("[Async delete_group error_code] : " + str(error_code))
    client.delete_group(1234, callback = MyDeleteGroupCallback())

    uids, error_code = client.get_group_members(123)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_group_members ok] : uids = " + str(uids))
    else:
        print("[Sync get_group_members error_code] : " + str(error_code))

    class MyGetGroupMembersCallback(GetGroupMembersCallback):
        def callback(self, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_group_members ok] : uids = " + str(uids))
            else:
                print("[Async get_group_members error_code] : " + str(error_code))
    client.get_group_members(123, callback = MyGetGroupMembersCallback())

    ok, error_code = client.is_group_member(123, 123456)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync is_group_member ok] ok = " + str(ok))
    else:
        print("[Sync is_group_member error_code] : " + str(error_code))

    class MyIsGroupMemberCallback(IsGroupMemberCallback):
        def callback(self, ok, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async is_group_member ok] ok = " + str(ok))
            else:
                print("[Async is_group_member error_code] : " + str(error_code))
    client.is_group_member(123, 123456, callback = MyIsGroupMemberCallback())

    gids, error_code = client.get_user_groups(123456)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_user_groups ok] : gids = " + str(gids))
    else:
        print("[Sync get_user_groups error_code] : " + str(error_code))

    class MyGetUserGroupsCallback(GetUserGroupsCallback):
        def callback(self, mtime, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_user_groups ok] : gids = " + str(gids))
            else:
                print("[Async get_user_groups error_code] : " + str(error_code))
    client.get_user_groups(123456, callback = MyGetUserGroupsCallback())

    error_code = client.add_group_ban(123, 123456789, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync add_group_ban ok]")
    else:
        print("[Sync add_group_ban error_code] : " + str(error_code))

    class MyAddGroupBanCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async add_group_ban ok]")
            else:
                print("[Async add_group_ban error_code] : " + str(error_code))
    client.add_group_ban(123, 123456789, 10, callback = MyAddGroupBanCallback())

    error_code = client.remove_group_ban(123, 123456789)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync remove_group_ban ok]")
    else:
        print("[Sync remove_group_ban error_code] : " + str(error_code))

    class MyRemoveGroupBanCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async remove_group_ban ok]")
            else:
                print("[Async remove_group_ban error_code] : " + str(error_code))
    client.remove_group_ban(123, 123456789, callback = MyRemoveGroupBanCallback())

    ok, error_code = client.is_ban_of_group(123, 123456)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync is_ban_of_group ok] ok = " + str(ok))
    else:
        print("[Sync is_ban_of_group error_code] : " + str(error_code))

    class MyIsBanOfGroupCallback(IsBanOfGroupCallback):
        def callback(self, ok, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async is_ban_of_group ok] ok = " + str(ok))
            else:
                print("[Async is_ban_of_group error_code] : " + str(error_code))
    client.is_ban_of_group(123, 123456, callback = MyIsBanOfGroupCallback())

    error_code = client.set_group_info(123, 'test_oinfo', 'test_pinfo')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync set_group_info ok]")
    else:
        print("[Sync set_group_info error_code] : " + str(error_code))

    class MySetGroupInfo(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async set_group_info ok]")
            else:
                print("[Async set_group_info error_code] : " + str(error_code))
    client.set_group_info(123, 'test_oinfo', 'test_pinfo', MySetGroupInfo())

    oinfo, pinfo, error = client.get_group_info(123)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_group_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
    else:
        print("[Sync get_group_info error_code] : " + str(error_code))

    class MyGetGroupInfoCallback(GetGroupInfoCallback):
        def callback(self, oinfo, pinfo, error):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_group_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
            else:
                print("[Async get_group_info error_code] : " + str(error_code))
    client.get_group_info(123, callback = MyGetGroupInfoCallback())

def test_room(client):
    error_code = client.add_room_ban(123, 123456789, 10)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync add_room_ban ok]")
    else:
        print("[Sync add_room_ban error_code] : " + str(error_code))

    class MyAddRoomBanCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async add_room_ban ok]")
            else:
                print("[Async add_room_ban error_code] : " + str(error_code))
    client.add_room_ban(123, 123456789, 10, callback = MyAddRoomBanCallback())

    error_code = client.remove_room_ban(123, 123456789)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync remove_room_ban ok]")
    else:
        print("[Sync remove_room_ban error_code] : " + str(error_code))

    class MyRemoveRoomBanCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async remove_room_ban ok]")
            else:
                print("[Async remove_room_ban error_code] : " + str(error_code))
    client.remove_room_ban(123, 123456789, callback = MyRemoveRoomBanCallback())

    ok, error_code = client.is_ban_of_room(123, 123456)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync is_ban_of_room ok] ok = " + str(ok))
    else:
        print("[Sync is_ban_of_room error_code] : " + str(error_code))

    class MyIsBanOfRoomCallback(IsBanOfRoomCallback):
        def callback(self, ok, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async is_ban_of_room ok] ok = " + str(ok))
            else:
                print("[Async is_ban_of_room error_code] : " + str(error_code))
    client.is_ban_of_room(123, 123456, callback = MyIsBanOfRoomCallback())

    error_code = client.add_room_member(123, 123456789)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync add_room_member ok]")
    else:
        print("[Sync add_room_member error_code] : " + str(error_code))

    class MyAddRoomMemberCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async add_room_member ok]")
            else:
                print("[Async add_room_member error_code] : " + str(error_code))
    client.add_room_member(123, 123456789, callback = MyAddRoomMemberCallback())

    error_code = client.delete_room_member(123, 123456789)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync delete_room_member ok]")
    else:
        print("[Sync delete_room_member error_code] : " + str(error_code))

    class MyDeleteRoomMemberCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async delete_room_member ok]")
            else:
                print("[Async delete_room_member error_code] : " + str(error_code))
    client.delete_room_member(123, 123456789, callback = MyDeleteRoomMemberCallback())

    error_code = client.set_room_info(123, 'test_oinfo', 'test_pinfo')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync set_room_info ok]")
    else:
        print("[Sync set_room_info error_code] : " + str(error_code))

    class MySetRoomInfo(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async set_room_info ok]")
            else:
                print("[Async set_room_info error_code] : " + str(error_code))
    client.set_room_info(123, 'test_oinfo', 'test_pinfo', MySetRoomInfo())

    oinfo, pinfo, error = client.get_room_info(123)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync get_room_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
    else:
        print("[Sync get_room_info error_code] : " + str(error_code))

    class MyGetRoomInfoCallback(GetRoomInfoCallback):
        def callback(self, oinfo, pinfo, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async get_room_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
            else:
                print("[Async get_room_info error_code] : " + str(error_code))
    client.get_room_info(123, callback = MyGetRoomInfoCallback())

def test_data(client):
    error_code = client.data_set(123, 'key', 'val')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync data_set ok]")
    else:
        print("[Sync data_set error_code] : " + str(error_code))

    class MyDataSetCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async data_set ok]")
            else:
                print("[Async data_set error_code] : " + str(error_code))
    client.data_set(123, 'key', 'val', callback = MyDataSetCallback())

    value, error_code = client.data_get(123, 'key')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync data_get ok] : value = " + value)
    else:
        print("[Sync data_get error_code] : " + str(error_code))

    class MyDataGetCallback(DataGetCallback):
        def callback(self, value, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async data_get ok] : value = " + value)
            else:
                print("[Async data_get error_code] : " + str(error_code))
    client.data_get(123, 'key', callback = MyDataGetCallback())

    error_code = client.data_delete(123, 'key')
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync data_delete ok]")
    else:
        print("[Sync data_delete error_code] : " + str(error_code))

    class MyDataDeleteCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async data_delete ok]")
            else:
                print("[Async data_delete error_code] : " + str(error_code))
    client.data_delete(123, 'key', callback = MyDataDeleteCallback())

def test_listen(client):

    error_code = client.set_all_listen(p2p = True, group = True, room = True, ev = True)
    if error_code == FPNN_ERROR.FPNN_EC_OK:
        print("[Sync set_all_listen ok]")
    else:
        print("[Sync set_all_listen error_code] : " + str(error_code))

    class MySetAllListenCallback(BasicCallback):
        def callback(self, error_code):
            if error_code == FPNN_ERROR.FPNN_EC_OK:
                print("[Async set_listen ok]")
            else:
                print("[Async set_listen error_code] : " + str(error_code))
    client.set_listen(gids = [11,22,33], rids = [44,55,66], uids = [77,88,99], events = ['login','logout'], callback = MySetAllListenCallback())

class MyErrorRecorder(ErrorRecorder):
    def record_error(self, message):
        print("error: " + message)

if  __name__ == "__main__":
    client = RTMServerClient(11000001, 'ef3617e5-e886-4a4e-9eef-7263c0320628', '161.189.171.91:13315')
    client.set_error_recorder(MyErrorRecorder())

    print(RTM_SDK_VERSION)
    print(RTM_INTERFACE_VERSION)
    print(FPNN_SDK_VERSION)

    class MyConnectionCallback(RTMConnectionCallback):
        def connected(self, connection_id, endpoint, connected, is_reconnect):
            print("connected", connection_id, endpoint, connected, is_reconnect)

        def closed(self, connection_id, endpoint, caused_by_error, is_reconnect):
            print("closed", connection_id, endpoint, caused_by_error, is_reconnect)

    client.set_connection_callback(MyConnectionCallback())

    class MyRTMServerPushMonitor(RTMServerPushMonitor):
        def __init__(self):
            pass

        def print_messagee(self, messag):
            print("from_uid: ", messag.from_uid)
            print("to_id: ", messag.to_id)
            print("message_type: ", message.message_type)
            print("message_id: ", message.message_id)
            print("message: ", message.message)
            print("attrs: ", message.attrs)
            print("modified_time: ", message.modified_time)
            if message.file_info != None:
                print("file_info.url: ", message.file_info.url)
                print("file_info.size: ", message.file_info.size)
                print("file_info.surl: ", message.file_info.surl)
                print("file_info.is_rtm_audio: ", message.file_info.is_rtm_audio)
                print("file_info.language: ", message.file_info.language)
                print("file_info.duration: ", message.file_info.duration)
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

    client.set_quest_processor(MyRTMServerPushMonitor())

    test_token_and_system(client)

    test_send_message(client)

    test_get_message(client)

    test_delete_message(client)

    test_get_message_info(client)

    test_send_chat(client)

    test_get_chat(client)

    test_translate(client)

    test_file(client)

    test_user(client)

    test_friend(client)

    test_group(client)

    test_room(client)

    test_data(client)

    test_listen(client)

    time.sleep(60)

    client.close()
    client.destory()