import time
import datetime
import subprocess

from module import nfc_reader as nr
from module import google_sheets as gs
from module import ignore as ign
from module import queue as que

path = '/'
file_success = 'audio/success.wav'
file_error = 'audio/error.wav'

ig = ign.ignore()

def on_connect(tag, qu):
    print('connect_card')
    dt_now = datetime.datetime.now()
    date = '{0}/{1}/{2}'.format(dt_now.year, dt_now.month, dt_now.day)
    tm = '{0}:{1}:{2}'.format(dt_now.hour, dt_now.minute, dt_now.second)

    lst = (tag, time.time())
    if ig.check(lst):
        subprocess.call('aplay {0}{1}'.format(path, file_success), shell=True)
        qu(gs.appendSheets, (date, tm, tag))
        # gs.appendSheets(value1=date, value2=tm, value3=tag)
        print('detect.')
    else:
        subprocess.call('aplay {0}{1}'.format(path, file_error), shell=True)
        print('err')
    ig.update(lst)

def main():
    with nr.suica_reader() as sr:
        qu = que.queue()
        itv = time.time()-30
        try:
            while True:
                sr.connect(on_connect, qu)

                time.sleep(sr.TIME_wait)
                if qu.exist() and time.time()<itv:
                    qu.execute()
                    itv=time.time()+15

        except KeyboardInterrupt:
            print('except: KeyboardInterrupt')

if __name__=='__main__':
    main()
    # print(time.time())