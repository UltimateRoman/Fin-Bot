import time, requests, json, urllib
from datetime import date

token = input("Enter telegram bot token:")
url = "https://api.telegram.org/bot"+token

budget = 0
exp_amount = 0
events = []

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
            args = text.split()

            if args[0] == "Hi":
                reply = "Hello, I'm FinBot👋"

            elif args[0] == "/start":
                reply = "Welcome!☺️ Use /help to get the list of supported commands"

            elif args[0] == "/help":
                reply = "Hey there! The following commands are supported - \n /budget [amount]- Set your monthly budget \n /spent [amount] [description]- Record a new expenditure event along with amount  \n /history - Shows all your expenditure events \n /view - View your total expenditure and available balance"

            elif args[0] == "/budget":
                global budget
                budget = int(args[1])
                reply = "Your monthly budget has been successfully set as $" + str(budget)
            
            elif args[0] == "/spent":
                global exp_amount
                global events
                event = {}
                event['amount'] = int(args[1])
                event['desc'] = args[2]
                events.append(event)
                exp_amount += event['amount']
                reply = "Successfully recorded new expenditure."

            elif args[0] == "/history":
                if events:
                    reply = "Expenditures for " + date.today().strftime("%B %d, %Y") + "\n"
                    for e in events:
                        reply += "$" + str(e['amount']) + " : " + e['desc']
                else:
                    reply = "No expenditure events have been recorded yet."

            elif args[0] == "/view":
                reply = "Total amount spent: $" + str(exp_amount) + "\n Available balance in your budget: $" + str(budget - exp_amount)

            elif args[0] == "Thanks":
                reply = "Goodbye! See you 😁"

            else:
                reply = text
            
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
