import binascii
import time

import nfc

class suica_reader:
    target_req_suica = nfc.clf.RemoteTarget('212F') # 212F(FeliCa)
    target_req_suica.sensf_req = bytearray.fromhex('0000030000') # 0003(Suica)

    def __init__(self):
        self.TEST_mode = False

        self.TIME_cycle = 0.1 # Suica待ち受けの1サイクル秒
        self.TIME_interval = 0.01 # Suica待ち受けの反応インターバル
        self.TIME_wait = 1 # タッチされてから次の待ち受けを開始するまで無効化する秒
        self.TIME_iterations = int(self.TIME_cycle//self.TIME_interval)+1

        self.clf = nfc.ContactlessFrontend('usb')
        if self.TEST_mode:
            print('__init__')
            print('TIME_cycle = ', self.TIME_cycle)
            print('TIME_interval = ', self.TIME_interval)
            print('TIME_wait = ', self.TIME_wait)
            print('TIME_iterations = ', self.TIME_iterations)

    def __enter__(self):
        if self.TEST_mode:
            print('__enter__')
        return self

    def __exit__(self, ex_type, ex_value, trace):
        if self.TEST_mode:
            print('__exit__')
        self.clf.close()

    def updateTimeIterations(self):
        self.TIME_iterations = int(self.TIME_cycle//self.TIME_interval)+1
        if self.TEST_mode:
            print('updateTimeIteratons')
            print('TIME_iterations = ', self.TIME_iterations)

    def setTimeCycle(self, time):
        self.TIME_cycle = time
        self.updateTimeIterations()
        if self.TEST_mode:
            print('setTimeCycle')
            print('TIME_cycle = ', self.TIME_cycle)

    def setTimeInterval(self, time):
        self.TIME_interval = time
        self.updateTimeIterations()
        if self.TEST_mode:
            print('setTimeInterval')
            print('TIME_interval = ', self.TIME_interval)

    def setTimeWait(self, time):
        self.TIME_wait = time
        if self.TEST_mode:
            print('setTimeWait')
            print('TIME_wait = ', self.TIME_wait)

    def connect(self, on_connect):
        print('suica waiting...')
        while True:
            target_res = self.clf.sense(self.target_req_suica, iterations=self.TIME_iterations, interval=self.TIME_interval)
            if target_res is not None:
                tag = nfc.tag.activate_tt3(self.clf, target_res)
                tag.sys = 3

                idm = binascii.hexlify(tag.idm)
                on_connect(idm)
                break


def on_connect(tag):
    print(tag)

def test():
    with suica_reader() as sr:
        try:
            while True:
                sr.connect(on_connect)

                time.sleep(sr.TIME_wait)
        except KeyboardInterrupt:
            print('KeyboardInterrupt')

            

if __name__=='__main__':
    test()
