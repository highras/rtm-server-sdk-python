# coding: utf-8
import time
from Rtm import RTMServerClient, DoneCallback

class MyDoneCallback(DoneCallback):
    def done(self):
        print("done")

    def onException(self, exception):
        print repr(exception)

def main():
    client = RTMServerClient(1000001, '3a0023b6-bc80-488d-b312-c4a139b5ab1a',
            '10.63.2.47:13315')

    client.sendMsg(1, 123, 51, "test msg", "test attrs", MyDoneCallback())

    time.sleep(2)
    client.close()

if __name__ == '__main__':
    main()
