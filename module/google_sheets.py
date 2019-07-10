import requests

IFTTT_URL = 'https://maker.ifttt.com/trigger/{0}/with/key/{1}'

def ifttt_webhook(key, eventid, payload):
    url = IFTTT_URL.format(eventid, key)
    response = requests.post(url, data=payload)
    print(response)

def appendRow(key, value1=None, value2=None, value3=None):
    eventid = 'attendance_event'
    payload = {"value1": value1,
                "value2": value2,
                "value3": value3}
    ifttt_webhook(key, eventid, payload)
    print(eventid, payload)

if __name__ == '__main__':
    date = '2019/06/11'
    time = '19:50'
    id = 'dhawa'
    payload = (date, time, id)

    appendRow('key', *payload)
