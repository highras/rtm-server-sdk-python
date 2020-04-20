#encoding=utf8
import sys
sys.path.append("../src")
import time
from rtm import *

def test_token_and_system(client):
    token, error = client.get_token(12345)
    if error == None:
        print("[Sync get_token ok] : token = " + token)
    else:
        print("[Sync get_token error] : " + str(error))

    class MyGetTokenCallback(GetTokenCallback):
        def callback(self, token, error):
            if error == None:
                print("[Async get_token ok] : token = " + token)
            else:
                print("[Async get_token error] : " + str(error))
    client.get_token(12345, callback = MyGetTokenCallback())

    error = client.kickout(12345)
    if error == None:
        print("[Sync kickout ok]")
    else:
        print("[Sync kickout error] : " + str(error))

    class MyKickoutCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async kickout ok]")
            else:
                print("[Async kickout error] : " + str(error))
    client.kickout(12345, callback = MyKickoutCallback())

    error = client.add_device(12345, 'apns', 'xxxxxxx')
    if error == None:
        print("[Sync add_device ok]")
    else:
        print("[Sync add_device error] : " + str(error))

    class MyAddDeviceCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async add_device ok]")
            else:
                print("[Async add_device error] : " + str(error))
    client.add_device(12345, 'apns', 'xxxxxxx', callback = MyAddDeviceCallback())

    error = client.remove_device(12345, 'xxxxxxx')
    if error == None:
        print("[Sync remove_device ok]")
    else:
        print("[Sync remove_device error] : " + str(error))

    class MyRemoveDeviceCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async remove_device ok]")
            else:
                print("[Async remove_device error] : " + str(error))
    client.remove_device(12345, 'xxxxxxx', callback = MyRemoveDeviceCallback())

    error = client.remove_token(12345)
    if error == None:
        print("[Sync remove_token ok]")
    else:
        print("[Sync remove_token error] : " + str(error))

    class MyRemoveTokenCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async remove_token ok]")
            else:
                print("[Async remove_token error] : " + str(error))
    client.remove_token(12345, callback = MyRemoveTokenCallback())
    
def test_send_message(client):
    mid, mtime, error = client.send_message(51, 123456, 654321, 'test msg', 'test attrs')
    if error == None:
        print("[Sync send_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_message error] : " + str(error))

    class MySendMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async send_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_message error] : " + str(error))
    client.send_message(51, 123456, 654321, 'test msg', 'test attrs', callback = MySendMessageCallback())

    mid, mtime, error = client.send_messages(51, 123456, [654321, 123], 'test msg', 'test attrs')
    if error == None:
        print("[Sync send_messages ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_messages error] : " + str(error))

    class MySendMessagesCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async send_messages ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_messages error] : " + str(error))
    client.send_messages(51, 123456, [654321, 123], 'test msg', 'test attrs', callback = MySendMessagesCallback())

    mid, mtime, error = client.send_group_message(51, 123456, 123, 'test msg', 'test attrs')
    if error == None:
        print("[Sync send_group_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_group_message error] : " + str(error))

    class MySendGroupMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async send_group_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_group_message error] : " + str(error))
    client.send_group_message(51, 123456, 123, 'test msg', 'test attrs', callback = MySendGroupMessageCallback())

    mid, mtime, error = client.send_room_message(51, 123456, 123, 'test msg', 'test attrs')
    if error == None:
        print("[Sync send_room_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_room_message error] : " + str(error))

    class MySendRoomMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async send_room_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_room_message error] : " + str(error))
    client.send_room_message(51, 123456, 123, 'test msg', 'test attrs', callback = MySendRoomMessageCallback())

    mid, mtime, error = client.broadcast_message(51, 111, 'test msg', 'test attrs')
    if error == None:
        print("[Sync broadcast_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync broadcast_message error] : " + str(error))

    class MyBroadcastMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async broadcast_message ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async broadcast_message error] : " + str(error))
    client.broadcast_message(51, 111, 'test msg', 'test attrs', callback = MyBroadcastMessageCallback())

def test_get_message(client):
    result, error = client.get_group_message(123456, 123, True, 10)
    if error == None:
        print("[Sync get_group_message ok] : num = " + str(result.num))
    else:
        print("[Sync get_group_message error] : " + str(error))

    class MyGetGroupMessageCallback(GetGroupMessageCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async get_group_message ok] : num = " + str(result.num))
            else:
                print("[Async get_group_message error] : " + str(error))
    client.get_group_message(123456, 123, True, 10, callback = MyGetGroupMessageCallback())

    result, error = client.get_room_message(123456, 123, True, 10)
    if error == None:
        print("[Sync get_room_message ok] : num = " + str(result.num))
    else:
        print("[Sync get_room_message error] : " + str(error))

    class MyGetRoomMessageCallback(GetRoomMessageCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async get_room_message ok] : num = " + str(result.num))
            else:
                print("[Async get_room_message error] : " + str(error))
    client.get_room_message(123456, 123, True, 10, callback = MyGetRoomMessageCallback())

    result, error = client.get_broadcast_message(111, True, 10)
    if error == None:
        print("[Sync get_broadcast_message ok] : num = " + str(result.num))
    else:
        print("[Sync get_broadcast_message error] : " + str(error))

    class MyGetBroadcastMessageCallback(GetBroadcastMessageCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async get_broadcast_message ok] : num = " + str(result.num))
            else:
                print("[Async get_broadcast_message error] : " + str(error))
    client.get_broadcast_message(111, True, 10, callback = MyGetBroadcastMessageCallback())

    result, error = client.get_p2p_message(123456, 654321, True, 10)
    if error == None:
        print("[Sync get_p2p_message ok] : num = " + str(result.num))
    else:
        print("[Sync get_p2p_message error] : " + str(error))

    class MyGetP2PMessageCallback(GetP2PMessageCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async get_p2p_message ok] : num = " + str(result.num))
            else:
                print("[Async get_p2p_message error] : " + str(error))
    client.get_p2p_message(123456, 654321, True, 10, callback = MyGetP2PMessageCallback())

def test_delete_message(client):
    error = client.delete_p2p_message(1111111, 12345, 654321)
    if error == None:
        print("[Sync delete_p2p_message ok]")
    else:
        print("[Sync delete_p2p_message error] : " + str(error))

    class MyDeleteP2PMessageCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async delete_p2p_message ok]")
            else:
                print("[Async delete_p2p_message error] : " + str(error))
    client.delete_p2p_message(1111111, 12345, 654321, callback = MyDeleteP2PMessageCallback())

    error = client.delete_group_message(1111111, 12345, 123)
    if error == None:
        print("[Sync delete_group_message ok]")
    else:
        print("[Sync delete_group_message error] : " + str(error))

    class MyDeleteGroupMessageCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async delete_group_message ok]")
            else:
                print("[Async delete_group_message error] : " + str(error))
    client.delete_group_message(1111111, 12345, 123, callback = MyDeleteGroupMessageCallback())

    error = client.delete_room_message(1111111, 12345, 123)
    if error == None:
        print("[Sync delete_room_message ok]")
    else:
        print("[Sync delete_room_message error] : " + str(error))

    class MyDeleteRoomMessageCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async delete_room_message ok]")
            else:
                print("[Async delete_room_message error] : " + str(error))
    client.delete_room_message(1111111, 12345, 123, callback = MyDeleteRoomMessageCallback())

    error = client.delete_broadcast_message(1111111, 111)
    if error == None:
        print("[Sync delete_broadcast_message ok]")
    else:
        print("[Sync delete_broadcast_message error] : " + str(error))

    class MyDeleteBroadcastMessageCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async delete_broadcast_message ok]")
            else:
                print("[Async delete_broadcast_message error] : " + str(error))
    client.delete_broadcast_message(1111111, 111, callback = MyDeleteBroadcastMessageCallback())

def test_get_message_info(client):
    result, error = client.get_p2p_message_info(1111111, 123456, 654321)
    if error == None:
        print("[Sync get_group_message ok] : msg = " + str(result.msg))
    else:
        print("[Sync get_group_message error] : " + str(error))

    class MyGetP2PMessageInfoCallback(GetMessageInfoCallback):
        def callback(self, result, error):
            if error == None:
                print("[Sync get_group_message ok] : msg = " + str(result.msg))
            else:
                print("[Sync get_group_message error] : " + str(error))
    client.get_p2p_message_info(1111111, 123456, 654321, callback = MyGetP2PMessageInfoCallback())

    result, error = client.get_group_message_info(1111111, 123456, 123)
    if error == None:
        print("[Sync get_group_message_info ok] : msg = " + str(result.msg))
    else:
        print("[Sync get_group_message_info error] : " + str(error))

    class MyGetGroupMessageInfoCallback(GetMessageInfoCallback):
        def callback(self, result, error):
            if error == None:
                print("[Sync get_group_message_info ok] : msg = " + str(result.msg))
            else:
                print("[Sync get_group_message_info error] : " + str(error))
    client.get_group_message_info(1111111, 123456, 123, callback = MyGetGroupMessageInfoCallback())

    result, error = client.get_room_message_info(1111111, 123456, 123)
    if error == None:
        print("[Sync get_room_message_info ok] : msg = " + str(result.msg))
    else:
        print("[Sync get_room_message_info error] : " + str(error))

    class MyGetRoomMessageInfoCallback(GetMessageInfoCallback):
        def callback(self, result, error):
            if error == None:
                print("[Sync get_room_message_info ok] : msg = " + str(result.msg))
            else:
                print("[Sync get_room_message_info error] : " + str(error))
    client.get_room_message_info(1111111, 123456, 123, callback = MyGetRoomMessageInfoCallback())

    result, error = client.get_broadcast_message_info(1111111, 123456)
    if error == None:
        print("[Sync get_broadcast_message_info ok] : msg = " + str(result.msg))
    else:
        print("[Sync get_broadcast_message_info error] : " + str(error))

    class MyGetBroadcastMessageInfoCallback(GetMessageInfoCallback):
        def callback(self, result, error):
            if error == None:
                print("[Sync get_broadcast_message_info ok] : msg = " + str(result.msg))
            else:
                print("[Sync get_broadcast_message_info error] : " + str(error))
    client.get_broadcast_message_info(1111111, 123456, callback = MyGetBroadcastMessageInfoCallback())

def test_send_chat(client):
    mid, mtime, error = client.send_chat(123456, 654321, 'test msg', 'test attrs')
    if error == None:
        print("[Sync send_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_chat error] : " + str(error))

    class MySendMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async send_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_chat error] : " + str(error))
    client.send_chat(123456, 654321, 'test msg', 'test attrs', callback = MySendMessageCallback())

    mid, mtime, error = client.send_chats( 123456, [654321, 123], 'test msg', 'test attrs')
    if error == None:
        print("[Sync send_chats ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_chats error] : " + str(error))

    class MySendMessagesCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async send_chats ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_chats error] : " + str(error))
    client.send_chats(123456, [654321, 123], 'test msg', 'test attrs', callback = MySendMessagesCallback())

    mid, mtime, error = client.send_group_chat(123456, 123, 'test msg', 'test attrs')
    if error == None:
        print("[Sync send_group_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_group_chat error] : " + str(error))

    class MySendGroupMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async send_group_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_group_chat error] : " + str(error))
    client.send_group_chat(123456, 123, 'test msg', 'test attrs', callback = MySendGroupMessageCallback())

    mid, mtime, error = client.send_room_chat(123456, 123, 'test msg', 'test attrs')
    if error == None:
        print("[Sync send_room_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync send_room_chat error] : " + str(error))

    class MySendRoomMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async send_room_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async send_room_chat error] : " + str(error))
    client.send_room_chat(123456, 123, 'test msg', 'test attrs', callback = MySendRoomMessageCallback())

    mid, mtime, error = client.broadcast_chat(111, 'test msg', 'test attrs')
    if error == None:
        print("[Sync broadcast_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
    else:
        print("[Sync broadcast_chat error] : " + str(error))

    class MyBroadcastMessageCallback(SendMessageCallback):
        def callback(self, mid, mtime, error):
            if error == None:
                print("[Async broadcast_chat ok] : mid = " + str(mid) + ' mtime = ' + str(mtime))
            else:
                print("[Async broadcast_chat error] : " + str(error))
    client.broadcast_chat(111, 'test msg', 'test attrs', callback = MyBroadcastMessageCallback())

def test_get_chat(client):
    result, error = client.get_group_chat(123456, 123, True, 10)
    if error == None:
        print("[Sync get_group_chat ok] : num = " + str(result.num))
    else:
        print("[Sync get_group_chat error] : " + str(error))

    class MyGetGroupMessageCallback(GetGroupMessageCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async get_group_chat ok] : num = " + str(result.num))
            else:
                print("[Async get_group_chat error] : " + str(error))
    client.get_group_chat(123456, 123, True, 10, callback = MyGetGroupMessageCallback())

    result, error = client.get_room_chat(123456, 123, True, 10)
    if error == None:
        print("[Sync get_room_chat ok] : num = " + str(result.num))
    else:
        print("[Sync get_room_chat error] : " + str(error))

    class MyGetRoomMessageCallback(GetRoomMessageCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async get_room_chat ok] : num = " + str(result.num))
            else:
                print("[Async get_room_chat error] : " + str(error))
    client.get_room_chat(123456, 123, True, 10, callback = MyGetRoomMessageCallback())

    result, error = client.get_broadcast_chat(111, True, 10)
    if error == None:
        print("[Sync get_broadcast_chat ok] : num = " + str(result.num))
    else:
        print("[Sync get_broadcast_chat error] : " + str(error))

    class MyGetBroadcastMessageCallback(GetBroadcastMessageCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async get_broadcast_chat ok] : num = " + str(result.num))
            else:
                print("[Async get_broadcast_chat error] : " + str(error))
    client.get_broadcast_chat(111, True, 10, callback = MyGetBroadcastMessageCallback())

    result, error = client.get_p2p_chat(123456, 654321, True, 10)
    if error == None:
        print("[Sync get_p2p_chat ok] : num = " + str(result.num))
    else:
        print("[Sync get_p2p_chat error] : " + str(error))

    class MyGetP2PMessageCallback(GetP2PMessageCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async get_p2p_chat ok] : num = " + str(result.num))
            else:
                print("[Async get_p2p_chat error] : " + str(error))
    client.get_p2p_chat(123456, 654321, True, 10, callback = MyGetP2PMessageCallback())

def test_translate(client):
    result, error = client.translate('hello world', 'zh-CN')
    if error == None:
        print("[Sync translate ok] : source = " + result.source + " target = " + result.target + " source_text = " + result.source_text + " target_text = " + result.target_text)
    else:
        print("[Sync translate error] : " + str(error))

    class MyTranslateCallback(TranslateCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async translate ok] : source = " + result.source + " target = " + result.target + " source_text = " + result.source_text + " target_text = " + result.target_text)
            else:
                print("[Async translate error] : " + str(error))
    client.translate('hello world', 'zh-CN', callback = MyTranslateCallback())

    result, error = client.profanity('出售，海洛因')
    if error == None:
        print("[Sync profanity ok] : text = " + result.text + " classification = " + str(result.classification))
    else:
        print("[Sync profanity error] : " + str(error))

    class MyProfanityCallback(ProfanityCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async profanity ok] : text = " + result.text + " classification = " + str(result.classification))
            else:
                print("[Async profanity error] : " + str(error))
    client.profanity('出售，海洛因', callback = MyProfanityCallback())

    result, error = client.transcribe('a test audio binary')
    if error == None:
        print("[Sync transcribe ok] : text = " + result.text + " lang = " + result.lang)
    else:
        print("[Sync transcribe error] : " + str(error))

    class MyTranscribeCallback(TranscribeCallback):
        def callback(self, result, error):
            if error == None:
                print("[Async transcribe ok] : text = " + result.text + " lang = " + result.lang)
            else:
                print("[Async transcribe error] : " + str(error))
    client.transcribe('a test audio binary', callback = MyTranscribeCallback())

def test_file(client):
    token, endpoint, error = client.file_token(123, 'sendfile', to = 1234)
    if error == None:
        print("[Sync file_token ok] : token = " + token + " endpoint = " + endpoint)
    else:
        print("[Sync file_token error] : " + str(error))

    class MyFileTokenCallback(FileTokenCallback):
        def callback(self, token, endpoint, error):
            if error == None:
                print("[Async file_token ok] : token = " + token + " endpoint = " + endpoint)
            else:
                print("[Async file_token error] : " + str(error))
    client.file_token(123, 'sendfile', to = 1234, callback = MyFileTokenCallback())

    mtime, error = client.send_file(123456, 654321, 40, '/Users/zhaojianjun/Downloads/audio1.bin')
    if error == None:
        print("[Sync send_file ok] : mtime = " + str(mtime))
    else:
        print("[Sync send_file error] : " + str(error))

    class MySendFileCallback(SendFileCallback):
        def callback(self, mtime, error):
            if error == None:
                print("[Async send_file ok] : mtime = " + str(mtime))
            else:
                print("[Async send_file error] : " + str(error))
    client.send_file(123456, 654321, 40, '/Users/zhaojianjun/Downloads/audio1.bin', callback = MySendFileCallback())

def test_user(client):
    uids, error = client.get_online_users([123, 456])
    if error == None:
        print("[Sync get_online_users ok] : uids = " + str(uids))
    else:
        print("[Sync get_online_users error] : " + str(error))

    class MyGetOnlineUsersCallback(GetOnlineUsersCallback):
        def callback(self, mtime, error):
            if error == None:
                print("[Async get_online_users ok] : uids = " + str(uids))
            else:
                print("[Async get_online_users error] : " + str(error))
    client.get_online_users([123, 456], callback = MyGetOnlineUsersCallback())

    error = client.add_project_black(123456789, 10)
    if error == None:
        print("[Sync add_project_black ok]")
    else:
        print("[Sync add_project_black error] : " + str(error))

    class MyAddProjectBlack(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async add_project_black ok]")
            else:
                print("[Async add_project_black error] : " + str(error))
    client.add_project_black(123456789, 10, callback = MyAddProjectBlack())

    ok, error = client.is_project_black(123456789)
    if error == None:
        print("[Sync is_project_black ok] ok = " + str(ok))
    else:
        print("[Sync is_project_black error] : " + str(error))

    class MyIsProjectBlackCallback(IsProjectBlackCallback):
        def callback(self, ok, error):
            if error == None:
                print("[Async is_project_black ok] ok = " + str(ok))
            else:
                print("[Async is_project_black error] : " + str(error))
    client.is_project_black(123456789, callback = MyIsProjectBlackCallback())

    error = client.set_user_info(123456789, 'test_oinfo', 'test_pinfo')
    if error == None:
        print("[Sync set_user_info ok]")
    else:
        print("[Sync set_user_info error] : " + str(error))

    class MySetUserInfo(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async set_user_info ok]")
            else:
                print("[Async set_user_info error] : " + str(error))
    client.set_user_info(123456789, 'test_oinfo', 'test_pinfo', MySetUserInfo())

    oinfo, pinfo, error = client.get_user_info(123456789)
    if error == None:
        print("[Sync get_user_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
    else:
        print("[Sync get_user_info error] : " + str(error))

    class MyGetUserInfoCallback(GetUserInfoCallback):
        def callback(self, oinfo, pinfo, error):
            if error == None:
                print("[Async get_user_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
            else:
                print("[Async get_user_info error] : " + str(error))
    client.get_user_info(123456789, callback = MyGetUserInfoCallback())

    info, error = client.get_user_open_info([123456789, 123456])
    if error == None:
        print("[Sync get_user_open_info ok] : info = " + str(info))
    else:
        print("[Sync get_user_open_info error] : " + str(error))

    class MyGetUserOpenInfoCallback(GetUserOpenInfoCallback):
        def callback(self, info, error):
            if error == None:
                print("[Async get_user_open_info ok] : info = " + str(info))
            else:
                print("[Async get_user_open_info error] : " + str(error))
    client.get_user_open_info([123456789, 123456], callback = MyGetUserOpenInfoCallback())

def test_friend(client):
    error = client.add_friends(123456789, [123, 456, 789])
    if error == None:
        print("[Sync add_friends ok]")
    else:
        print("[Sync add_friends error] : " + str(error))

    class MyAddFriendsCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async add_friends ok]")
            else:
                print("[Async add_friends error] : " + str(error))
    client.add_friends(123456789, [123, 456, 789], callback = MyAddFriendsCallback())

    error = client.delete_friends(123456789, [123])
    if error == None:
        print("[Sync delete_friends ok]")
    else:
        print("[Sync delete_friends error] : " + str(error))

    class MyDeleteFriendsCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async delete_friends ok]")
            else:
                print("[Async delete_friends error] : " + str(error))
    client.delete_friends(123456789, [123], callback = MyDeleteFriendsCallback())

    uids, error = client.get_friends(123456789)
    if error == None:
        print("[Sync get_friends ok] : uids = " + str(uids))
    else:
        print("[Sync get_friends error] : " + str(error))

    class MyGetFriendsCallback(GetFriendsCallback):
        def callback(self, mtime, error):
            if error == None:
                print("[Async get_friends ok] : uids = " + str(uids))
            else:
                print("[Async get_friends error] : " + str(error))
    client.get_friends(123456789, callback = MyGetFriendsCallback())

    ok, error = client.is_friend(123456789, 789)
    if error == None:
        print("[Sync is_friend ok] ok = " + str(ok))
    else:
        print("[Sync is_friend error] : " + str(error))

    class MyIsFriendCallback(IsFriendCallback):
        def callback(self, ok, error):
            if error == None:
                print("[Async is_friend ok] ok = " + str(ok))
            else:
                print("[Async is_friend error] : " + str(error))
    client.is_friend(123456789, 789, callback = MyIsFriendCallback())

    fuids, error = client.is_friends(123456789, [666, 789])
    if error == None:
        print("[Sync is_friends ok] : fuids = " + str(fuids))
    else:
        print("[Sync is_friends error] : " + str(error))

    class MyIsFriendsCallback(IsFriendsCallback):
        def callback(self, fuids, error):
            if error == None:
                print("[Async is_friends ok] : fuids = " + str(fuids))
            else:
                print("[Async is_friends error] : " + str(error))
    client.is_friends(123456789, [666, 789], callback = MyIsFriendsCallback())

def test_group(client):
    error = client.add_group_members(123, [123456789, 666, 888])
    if error == None:
        print("[Sync add_group_members ok]")
    else:
        print("[Sync add_group_members error] : " + str(error))

    class MyAddGroupMembersCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async add_group_members ok]")
            else:
                print("[Async add_group_members error] : " + str(error))
    client.add_group_members(123, [123456789, 666, 888], callback = MyAddGroupMembersCallback())

    error = client.delete_group_members(123, [123456789, 888])
    if error == None:
        print("[Sync delete_group_members ok]")
    else:
        print("[Sync delete_group_members error] : " + str(error))

    class MyDeleteGroupMembersCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async delete_group_members ok]")
            else:
                print("[Async delete_group_members error] : " + str(error))
    client.delete_group_members(123, [123456789, 888], callback = MyDeleteGroupMembersCallback())

    error = client.delete_group(1234)
    if error == None:
        print("[Sync delete_group ok]")
    else:
        print("[Sync delete_group error] : " + str(error))

    class MyDeleteGroupCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async delete_group ok]")
            else:
                print("[Async delete_group error] : " + str(error))
    client.delete_group(1234, callback = MyDeleteGroupCallback())

    uids, error = client.get_group_members(123)
    if error == None:
        print("[Sync get_group_members ok] : uids = " + str(uids))
    else:
        print("[Sync get_group_members error] : " + str(error))

    class MyGetGroupMembersCallback(GetGroupMembersCallback):
        def callback(self, mtime, error):
            if error == None:
                print("[Async get_group_members ok] : uids = " + str(uids))
            else:
                print("[Async get_group_members error] : " + str(error))
    client.get_group_members(123, callback = MyGetGroupMembersCallback())

    ok, error = client.is_group_member(123, 123456)
    if error == None:
        print("[Sync is_group_member ok] ok = " + str(ok))
    else:
        print("[Sync is_group_member error] : " + str(error))

    class MyIsGroupMemberCallback(IsGroupMemberCallback):
        def callback(self, ok, error):
            if error == None:
                print("[Async is_group_member ok] ok = " + str(ok))
            else:
                print("[Async is_group_member error] : " + str(error))
    client.is_group_member(123, 123456, callback = MyIsGroupMemberCallback())

    gids, error = client.get_user_groups(123456)
    if error == None:
        print("[Sync get_user_groups ok] : gids = " + str(gids))
    else:
        print("[Sync get_user_groups error] : " + str(error))

    class MyGetUserGroupsCallback(GetUserGroupsCallback):
        def callback(self, mtime, error):
            if error == None:
                print("[Async get_user_groups ok] : gids = " + str(gids))
            else:
                print("[Async get_user_groups error] : " + str(error))
    client.get_user_groups(123456, callback = MyGetUserGroupsCallback())

    error = client.add_group_ban(123, 123456789, 10)
    if error == None:
        print("[Sync add_group_ban ok]")
    else:
        print("[Sync add_group_ban error] : " + str(error))

    class MyAddGroupBanCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async add_group_ban ok]")
            else:
                print("[Async add_group_ban error] : " + str(error))
    client.add_group_ban(123, 123456789, 10, callback = MyAddGroupBanCallback())

    error = client.remove_group_ban(123, 123456789)
    if error == None:
        print("[Sync remove_group_ban ok]")
    else:
        print("[Sync remove_group_ban error] : " + str(error))

    class MyRemoveGroupBanCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async remove_group_ban ok]")
            else:
                print("[Async remove_group_ban error] : " + str(error))
    client.remove_group_ban(123, 123456789, callback = MyRemoveGroupBanCallback())

    ok, error = client.is_ban_of_group(123, 123456)
    if error == None:
        print("[Sync is_ban_of_group ok] ok = " + str(ok))
    else:
        print("[Sync is_ban_of_group error] : " + str(error))

    class MyIsBanOfGroupCallback(IsBanOfGroupCallback):
        def callback(self, ok, error):
            if error == None:
                print("[Async is_ban_of_group ok] ok = " + str(ok))
            else:
                print("[Async is_ban_of_group error] : " + str(error))
    client.is_ban_of_group(123, 123456, callback = MyIsBanOfGroupCallback())

    error = client.set_group_info(123, 'test_oinfo', 'test_pinfo')
    if error == None:
        print("[Sync set_group_info ok]")
    else:
        print("[Sync set_group_info error] : " + str(error))

    class MySetGroupInfo(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async set_group_info ok]")
            else:
                print("[Async set_group_info error] : " + str(error))
    client.set_group_info(123, 'test_oinfo', 'test_pinfo', MySetGroupInfo())

    oinfo, pinfo, error = client.get_group_info(123)
    if error == None:
        print("[Sync get_group_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
    else:
        print("[Sync get_group_info error] : " + str(error))

    class MyGetGroupInfoCallback(GetGroupInfoCallback):
        def callback(self, oinfo, pinfo, error):
            if error == None:
                print("[Async get_group_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
            else:
                print("[Async get_group_info error] : " + str(error))
    client.get_group_info(123, callback = MyGetGroupInfoCallback())

def test_room(client):
    error = client.add_room_ban(123, 123456789, 10)
    if error == None:
        print("[Sync add_room_ban ok]")
    else:
        print("[Sync add_room_ban error] : " + str(error))

    class MyAddRoomBanCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async add_room_ban ok]")
            else:
                print("[Async add_room_ban error] : " + str(error))
    client.add_room_ban(123, 123456789, 10, callback = MyAddRoomBanCallback())

    error = client.remove_room_ban(123, 123456789)
    if error == None:
        print("[Sync remove_room_ban ok]")
    else:
        print("[Sync remove_room_ban error] : " + str(error))

    class MyRemoveRoomBanCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async remove_room_ban ok]")
            else:
                print("[Async remove_room_ban error] : " + str(error))
    client.remove_room_ban(123, 123456789, callback = MyRemoveRoomBanCallback())

    ok, error = client.is_ban_of_room(123, 123456)
    if error == None:
        print("[Sync is_ban_of_room ok] ok = " + str(ok))
    else:
        print("[Sync is_ban_of_room error] : " + str(error))

    class MyIsBanOfRoomCallback(IsBanOfRoomCallback):
        def callback(self, ok, error):
            if error == None:
                print("[Async is_ban_of_room ok] ok = " + str(ok))
            else:
                print("[Async is_ban_of_room error] : " + str(error))
    client.is_ban_of_room(123, 123456, callback = MyIsBanOfRoomCallback())

    error = client.add_room_member(123, 123456789)
    if error == None:
        print("[Sync add_room_member ok]")
    else:
        print("[Sync add_room_member error] : " + str(error))

    class MyAddRoomMemberCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async add_room_member ok]")
            else:
                print("[Async add_room_member error] : " + str(error))
    client.add_room_member(123, 123456789, callback = MyAddRoomMemberCallback())

    error = client.delete_room_member(123, 123456789)
    if error == None:
        print("[Sync delete_room_member ok]")
    else:
        print("[Sync delete_room_member error] : " + str(error))

    class MyDeleteRoomMemberCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async delete_room_member ok]")
            else:
                print("[Async delete_room_member error] : " + str(error))
    client.delete_room_member(123, 123456789, callback = MyDeleteRoomMemberCallback())

    error = client.set_room_info(123, 'test_oinfo', 'test_pinfo')
    if error == None:
        print("[Sync set_room_info ok]")
    else:
        print("[Sync set_room_info error] : " + str(error))

    class MySetRoomInfo(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async set_room_info ok]")
            else:
                print("[Async set_room_info error] : " + str(error))
    client.set_room_info(123, 'test_oinfo', 'test_pinfo', MySetRoomInfo())

    oinfo, pinfo, error = client.get_room_info(123)
    if error == None:
        print("[Sync get_room_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
    else:
        print("[Sync get_room_info error] : " + str(error))

    class MyGetRoomInfoCallback(GetRoomInfoCallback):
        def callback(self, oinfo, pinfo, error):
            if error == None:
                print("[Async get_room_info ok] : oinfo = " + str(oinfo) + " pinfo = " + str(oinfo))
            else:
                print("[Async get_room_info error] : " + str(error))
    client.get_room_info(123, callback = MyGetRoomInfoCallback())

def test_data(client):
    error = client.data_set(123, 'key', 'val')
    if error == None:
        print("[Sync data_set ok]")
    else:
        print("[Sync data_set error] : " + str(error))

    class MyDataSetCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async data_set ok]")
            else:
                print("[Async data_set error] : " + str(error))
    client.data_set(123, 'key', 'val', callback = MyDataSetCallback())

    value, error = client.data_get(123, 'key')
    if error == None:
        print("[Sync data_get ok] : value = " + value)
    else:
        print("[Sync data_get error] : " + str(error))

    class MyDataGetCallback(DataGetCallback):
        def callback(self, value, error):
            if error == None:
                print("[Async data_get ok] : value = " + value)
            else:
                print("[Async data_get error] : " + str(error))
    client.data_get(123, 'key', callback = MyDataGetCallback())

    error = client.data_delete(123, 'key')
    if error == None:
        print("[Sync data_delete ok]")
    else:
        print("[Sync data_delete error] : " + str(error))

    class MyDataDeleteCallback(BasicCallback):
        def callback(self, error):
            if error == None:
                print("[Async data_delete ok]")
            else:
                print("[Async data_delete error] : " + str(error))
    client.data_delete(123, 'key', callback = MyDataDeleteCallback())

def test_listen(client):
    error = client.set_all_listen(p2p = True, group = True, room = True, ev = True)
    if error == None:
        print("[Sync set_all_listen ok]")
    else:
        print("[Sync set_all_listen error] : " + str(error))

if  __name__=="__main__":
    client = RTMServerClient(11000001, 'ef3617e5-e886-4a4e-9eef-7263c0320628', '52.82.27.68:13315', True, 10 * 1000)

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
    
    time.sleep(10)
    #time.sleep(1000)

    client.close()
    client.destory()