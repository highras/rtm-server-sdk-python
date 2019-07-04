# coding: utf-8
import time
from Rtm import RTMServerClient, DoneCallback

class MyDoneCallback(DoneCallback):
    def done(self):
        print("done")

    def onException(self, exception):
        print repr(exception)

def main():
    client = RTMServerClient(11000006, 'xxxxx-xxxx-xxxx-xxx-xxxxxx', '52.83.245.22:13315')

    client.sendMessage(1, 2, 51, "test msg", "test attrs", MyDoneCallback())

    print client.isBanOfRoomSync(1, 1)

    time.sleep(1)
    client.close()

if __name__ == '__main__':
    main()
