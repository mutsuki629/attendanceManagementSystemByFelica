from time import time
from time import sleep
from datetime import datetime
import subprocess
from queue import Queue

from module.nfc_reader import suica_reader
from module import google_sheets as sheets

PATH = '/home/mitsu10shi/amsf'
IFTTT_KEY = 'cO9Fnab5t3KimvSWjQERft'
SEND_ITV = 15

WAV_SUCCESS = '{0}/audio/success.wav'.format(PATH)
WAV_ERROR = '{0}/audi/error.wav'.format(PATH)

ignore = {}
req_queue = Queue()

def on_connect(tag):
    print('connect card')
    idm = tag

    if idm in ignore and ignore[idm]>time():
        subprocess.call('asplay {0}'.format(WAV_ERROR), shell=True)
        print('err')
    else:
        subprocess.call('asplay {0}'.format(WAV_SUCCESS), shell=True)
        ignore[idm]=time()+300
        print('detect')    

        current = datetime.now()
        cdate = '{0}/{1}/{2}'.format(current.year,
                                    current.month,
                                    current.day)
        ctime = '{0}:{1}:{2}'.format(current.hour,
                                    current.minute,
                                    current.second)
        
        req_queue.put((idm, cdate, ctime))
    
def pushSheets(arg):
    sheets.appendRow(IFTTT_KEY, *arg)

def main():
    with suica_reader() as sr:
        connect_flag=0
        connect_itv=time()
        send_flag=0
        send_itv=time()
        try:
            while True:
                if connect_flag==0:
                    idm = sr.sense()
                    if idm is not None:
                        on_connect(idm)
                        connect_flag=1
                        connect_itv=time()+sr.TIME_wait
                elif connect_itv<time():
                    connect_flag=0

                if send_flag==0:
                    if not req_queue.empty():
                        pushSheets(req_queue.get())
                        send_flag=1
                        send_itv=time()+SEND_ITV
                elif send_itv<time():
                    send_flag=0
                sleep(0.010)

        except KeyboardInterrupt:
            print('except: KeyboardInterrupt')


def test1():
    date = '2019/06/11'
    time = '19:50'
    idm = 'dahdowada'
    paylaod = (date, time, idm)
    sheets.appendRow(IFTTT_KEY, paylaod)

def test2():
    with suica_reader() as sr:
        try:
            while True:
                sr.connect(on_connect)
                sleep(sr.TIME_wait)
        except KeyboardInterrupt:
            print('except: KeyboardInterrupt')

def test3():
    d = {}
    if '0' in d and d['0']<30:
        print('a')

if __name__=='__main__':
    main()     

