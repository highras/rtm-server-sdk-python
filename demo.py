# coding: utf-8
import time
from Rtm import RTMServerClient, DoneCallback

class MyDoneCallback(DoneCallback):
    def done(self):
        print("done")

    def onException(self, exception):
        print repr(exception)

def main():
    client = RTMServerClient(1000008, 'test-key',
            '117.50.4.158:13315')

    client.sendMessage(1, 2, 51, "test msg", "test attrs", MyDoneCallback())

    time.sleep(1)
    client.close()

if __name__ == '__main__':
    main()
