try:
    from pyrogram import Client as yri
except ImportError:
    from subprocess import call
    from sys import platform as p
    if p == "linux" or p == "linux2":
        pip = "pip3"
    elif p == "darwin" or p == "win32":
        pip = "pip"
    call(f"{pip} install pyrogram",shell=True)
    from pyrogram import Client as yri
chat_id_input = input('enter group chat_id or group public username: ')
try:
    chat_id = int(chat_id_input)
except ValueError:
    chat_id = chat_id_input
id = int(input('enter api_id: '))
hash = input('enter api_hash: ')
yuri = yri(
    "wasyori",
    api_id = id, 
    api_hash = hash)
response_1 = ["متاكد تبي تستثمر","تعال بعد","استثمار ناجح!","حظ اوفر"]
response_2 = ["رصيدك الحين:","بينزل بعد",'فلوسك']
payload = ['راتب',"فلوسي","استثمار"]
from time import sleep
from json import loads
def answer_callback(chat_id,id,callback):
    try:
        yuri.request_callback_answer(
            chat_id=chat_id,
            message_id=id,
            callback_data=callback)
    except Exception:
        pass
def getting_money(message,split_word):
    return message.split(split_word)[1]\
        .split('ريال')[0].replace(" ",'')
def getting_time(message,split_word):
    str_time = message.split(split_word)[1]\
        .split('دقيقة')[0].replace(" ",'')
    return (int(str_time.split(':')[0])*60)+\
        int(str_time.split(':')[1])
def find_message():
    for message in yuri.get_chat_history(chat_id,1):
        return message,str(message)
def find_message_inline() -> str:
    for message in yuri.get_chat_history(chat_id,1):
        message = loads(str(message.reply_markup))["inline_keyboard"]
        try: 
            if message[0][0]["text"].__contains__('اي'):
                index = 0
            elif message[1][0]["text"].__contains__('اي'):
                index = 1
            return message[index][0]["callback_data"]
        except Exception as e:
            if message[0][0]["text"].__contains__('اي'):
                index = 0
            elif message[0][1]["text"].__contains__('اي'):
                index = 1
            return message[0][index]["callback_data"]
def sending_message(message):
    return yuri.send_message(chat_id,message)

def run_until_find(message):
    run = True
    sleep(5)
    while run:
        for message_dict in yuri.get_chat_history(chat_id,1):
            message_str = str(message_dict)
        for wanted_message in message:
            if message_str.__contains__(wanted_message):
                run = False
                return message_dict,message_str
            else:
                sleep(5)  
def main():
    while 1:
        sl = 50
        yuri.start()
        sending_message(payload[0])
        message = run_until_find(response_2)
        if message[1].__contains__(response_2[0]):
            money = getting_money(message[1],response_2[0])
            sending_message(f"{payload[2]} {money}",)
            message = run_until_find(response_1)
            if message[1].__contains__(response_1[0]):
                answer_callback(message[0].chat.id,message[0].id,find_message_inline())
                sl = 600
            elif message[1].__contains__(response_1[1]):
                sl = getting_time(message[1],response_1[1])
            elif message[1].__contains__(response_1[2]) \
                or message[1].__contains__(response_1[3]):
                sl = 600
        elif message[1].__contains__(response_2[1]):
            sl = getting_time(message[1],response_2[1])
            sending_message(payload[1])
            message = run_until_find(response_2)
            if message[1].__contains__(response_2[2]):
                money = getting_money(message[1],response_2[2])
                sending_message(f"{payload[2]} {money}")
                message = run_until_find(response_1)
                if message[1].__contains__(response_1[0]):
                    answer_callback(message[0].chat.id,message[0].id,find_message_inline())
                    sl = 600
                elif message[1].__contains__(response_1[1]):
                    sl = getting_time(message[1],response_1[1])
                elif message[1].__contains__(response_1[2])\
                    or message[1].__contains__(response_1[3]):
                    sl = 600
        yuri.send_message(chat_id,f"راح انتظر تقريباً {sl//60} دقيقة")
        yuri.stop()
        sleep(sl)
yuri.run(main())
