import binascii

import nfc

def connected(tag):
    pass

if __name__=='__main__':
    with nfc.ContactlessFrontend as clf:
        print(clf)
        if clf:
            while True:
                tag = clf.connect(rdqr={
                    'on-connect': lambda tag: False,
                })
            print(tag)
