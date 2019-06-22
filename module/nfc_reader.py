import binascii
import time

import nfc

TIME_cycle = 1.0 # Suica待ち受けの1サイクル秒
TIME_interval = 0.2 # Suica待ち受けの反応インターバル
TIME_wait = 3 # タッチされてから次の待ち受けを開始するまで無効化する秒

target_req_suica = nfc.clf.RemoteTarget('212F') # 212F(FeliCa)
target_req_suica.sensf_req = bytearray.fromhex('0000030000') # 0003(Suica)

def main():
    with nfc.ContactlessFrontend('usb') as clf:
        while True:
            target_res = clf.sense(target_req_suica, iterations=int(TIME_cycle//TIME_interval)+1, interval=TIME_interval)
            if target_res is not None:
                tag = nfc.tag.activate_tt3(clf, target_res)
                tag.sys= 3

                idm = binascii.hexlify(tag.idm)
                print('Suica detected. idm = ', idm)

                time.sleep(TIME_wait)

if __name__=='__main__':
    main()
