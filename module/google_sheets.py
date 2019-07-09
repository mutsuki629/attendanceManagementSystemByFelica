import requests

def ifttt_webhook(eventid, payload):

    url = "https://maker.ifttt.com/trigger/" + eventid + "/with/key/cO9Fnab5t3KimvSWjQERft"
    response = requests.post(url, data=payload)
    print(response)

def appendSheets(value1=None, value2=None, value3=None):
    eventid = 'attendance_event'
    payload = {"value1": value1,
                "value2": value2,
                "value3": value3}

    ifttt_webhook(eventid, payload)

# ここからスタート
if __name__ == '__main__':
        print ("IFTTT連携開始")

        date = '2019/06/11'
        time = '19:50'
        id = 'dhandhawou'

        appendSheets(date, time, id)

        print ("IFTTT連携終了")