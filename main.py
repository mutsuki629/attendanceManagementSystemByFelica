import time

from module import nfc_reader as nr

def on_connect(tag):
    print(tag)

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