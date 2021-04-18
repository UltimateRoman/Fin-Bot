import time, requests, json, urllib

token = input("Enter telegram bot token:")
url = "https://api.telegram.org/bot"+token

def get_message(offset):
    if offset:
        resp = requests.get(url+"/getUpdates?timeout=100&offset={}".format(offset))
    else:
        resp = requests.get(url+"/getUpdates?timeout=100")
    respd = json.loads(resp.content.decode("utf8"))
    return respd

def get_last_upid(respd):
    upids=[]
    for msg in respd['result']:
        upids.append(int(msg['update_id']))
    return max(upids)

def make_msg(respd):
    for msg in respd['result']:
        try:
            text = msg['message']['text']
            chat_id = msg['message']['chat']['id']
            print(text)
            if text == "Hi":
                reply="Hello, I'm FinBot👋"
            
            send_message(reply, chat_id)
        except Exception as e:
            print(e)

def send_message(reply, chat_id):
    reply = urllib.parse.quote_plus(reply)
    resp = requests.get(url+"/sendMessage?text={}&chat_id={}".format(reply, chat_id))
    rem = json.loads(resp.content.decode("utf8"))
    print("Replied to:", rem['result']['chat']['first_name'])


def main():
    last_upid = None
    t1 = time.time()
    while True:
        try:
            t2 = time.time()
            if t2-t1>20:
                t1 = time.time()
            respd = get_message(last_upid)
            if len(respd['result'])>0:
                last_upid = get_last_upid(respd)+1
                make_msg(respd)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(5)


if __name__ == '__main__':
    main()
