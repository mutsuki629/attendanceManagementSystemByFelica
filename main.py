import time
import datetime

from module import nfc_reader as nr
from module import google_sheets as gs
from module import ignore

ig = ignore()

def on_connect(tag):
    print('connect_card')
    dt_now = datetime.datetime.now()
    date = '{0}/{1}/{2}'.format(dt_now.year, dt_now.month, dt_now.day)
    tm = '{0}:{1}:{2}'.format(dt_now.hour, dt_now.minute, dt_now.second)

    lst = (tag, time.time())
    if ig.check(lst):
        gs.appendSheets(value1=date, value2=tm, value3=tag)
    ig.update(lst)

def main():
    with nr.suica_reader() as sr:
        try:
            while True:
                sr.connect(on_connect)

                time.sleep(sr.TIME_wait)
        except KeyboardInterrupt:
            print('except: KeyboardInterrupt')

if __name__=='__main__':
    main()