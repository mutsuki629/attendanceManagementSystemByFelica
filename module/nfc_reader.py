import binascii
from time import time

import nfc

class suica_reader:
    target_req_suica = nfc.clf.RemoteTarget('212F')
    target_req_suica.sensf_req = bytearray.fromhex('0000030000')

    def __init__(self):
        self.TIME_cycle = 0.1 # Suica待ち受けの1サイクル秒
        self.TIME_interval = 0.01 # Suica待ち受けの反応インターバル
        self.TIME_wait = 2 # タッチされてから次の待ち受けを開始するまで無効化する秒
        self.TIME_iterations = int(self.TIME_cycle//self.TIME_interval)+1

        self.clf = nfc.ContactlessFrontend('usb')
        print('TIME_cycle = ', self.TIME_cycle)
        print('TIME_interval = ', self.TIME_interval)
        print('TIME_wait = ', self.TIME_wait)
        print('TIME_iterations = ', self.TIME_iterations)

    def __enter__(self):
        return self
    
    def __exit__(self, ex_type, ex_value, trace):
        self.clf.close()

    def updateTimeIterations(self):
        self.TIME_iterations = int(self.TIME_cycle//self.TIME_interval)+1
        print('TIME_iterations = ', self.TIME_iterations)

    def setTimeCycle(self, time):
        self.TIME_cycle = time
        print('TIME_wait = ', self.TIME_wait)

    def setTimeInterval(self, time):
        self.TIME_interval = time
        self.updateTimeIterations()
        print('TIME_interval = ', self.TIME_interval)

    def setTimeWait(self, time):
        self.TIME_wait = time
        print('TIME_wait = ', self.TIME_wait)

    def sense(self):
        target_res = self.clf.sense(self.target_req_suica,
                                    iterations=self.TIME_iterations,
                                    interval=self.TIME_interval)
        if target_res is not None:
            tag = nfc.tag.activate_tt3(self.clf, target_res)
                tag.sys = 3
                idm = binascii.hexlify(tag.idm)
                return(idm)
        return None

    def connect(self, on_connect):
        print('suica waiting...')
        while True:
            target_res = self.clf.sense(self.target_req_suica,
                                        iterations=self.TIME_iterations,
                                        interval=self.TIME_interval)
            if target_res is not None:
                tag = nfc.tag.activate_tt3(self.clf, target_res)
                tag.sys = 3
                idm = binascii.hexlify(tag.idm)
                on_connect(idm)
                break