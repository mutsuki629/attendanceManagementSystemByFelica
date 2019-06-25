import time
import datetime

from module import nfc_reader as nr
from module import google_sheets as gs

def on_connect(tag):
    dt_now = datetime.datetime.now()
    date = '{0}/{1}/{2}'.format(dt_now.year, dt_now.month, dt_now.day)
    time = '{0}:{1}:{2}'.format(dt_now.hour, dt_now.minute, dt_now.second)


    print(date, time, tag)

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