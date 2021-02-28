import telebot
from telebot import types
import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing
import re
import time
from call import *

campaigns = [1]
#ID 泻邪屑锌邪薪懈泄 锌芯 芯斜蟹胁芯薪褍

TOKEN = "1650886927:AAG6dpNYWGfXeIdGNJcJA3EPWnZT3r5Ctzk"
#孝芯泻械薪 斜芯褌邪 胁 Telegram
bot = telebot.TeleBot(TOKEN)
#袗胁褌芯褉懈蟹褍械屑褋褟 锌芯 褌芯泻械薪褍

hello_text = "袩褉懈胁械褌! 馃憢 \n\n小芯 屑薪芯泄 褌褘 屑芯卸械褕褜 芯褉懈谐懈薪邪谢褜薪芯 褉邪蟹褘谐褉邪褌褜 褋胁芯懈褏 写褉褍蟹械泄 懈 蟹薪邪泻芯屑褘褏, 懈 泻邪泻 褋谢械写褍械褌 锌芯褋屑械褟褌褜褋褟 馃槃 \n\n袣邪泻 蟹邪泻邪蟹邪褌褜 蟹胁芯薪芯泻: \n\n1. 袙褘斜械褉懈 锌芯薪褉邪胁懈胁褕懈泄褋褟 褉芯蟹褘谐褉褘褕 褋褉械写懈 邪褍写懈芯蟹邪锌懈褋械泄 馃帀 \n\n2. 袙胁械写懈 薪芯屑械褉 褌械谢械褎芯薪邪 褔械谢芯胁械泻邪, 泻芯褌芯褉芯谐芯 褏芯褔械褕褜 褉邪蟹褘谐褉邪褌褜 馃摓 \n\n3. 袩芯锌芯谢薪懈 斜邪谢邪薪褋 薪邪 15 褉褍斜谢械泄 锌褉懈 锌芯屑芯褖懈 褍写芯斜薪芯泄 褋褋褘谢泻懈 鈿★笍 \n\n4. 袨卸懈写邪泄 胁 褌械褔械薪懈械 2 屑懈薪褍褌 谐芯谢芯褋芯胁芯械 褋芯芯斜褖械薪懈械 褋 蟹邪锌懈褋褜褞 褉邪蟹谐芯胁芯褉邪  \n\n袝褋谢懈 褔械谢芯胁械泻 薪械 斜械褉褢褌 褌褉褍斜泻褍, 写械薪褜谐懈 薪械 褋锌懈褕褍褌褋褟, 懈 褍 胁邪褋 斜褍写械褌 胁芯蟹屑芯卸薪芯褋褌褜 胁褘斜褉邪褌褜 写褉褍谐芯泄 薪芯屑械褉 褌械谢械褎芯薪邪"
#袩褉懈胁械褌褋褌胁械薪薪褘泄 褌械泻褋褌

def getJokesKeyboard(chat_id):
    #肖褍薪泻褑懈褟 锌芯谢褍褔械薪懈褟 写芯褋褌褍锌薪褘褏 褉芯蟹褘谐褉褘褕械泄
    with closing(pymysql.connect(host='localhost', user='root', password='', db='callprank', charset='utf8mb4', cursorclass=DictCursor)) as conn:
        with conn.cursor() as cur:
            sql = ("SELECT * FROM jokes ORDER BY id")
            cur.execute(sql)
            jokes = cur.fetchall()
            
    jokesKeyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
    #袣谢邪胁懈邪褌褍褉邪 胁褘斜芯褉邪 锌褉邪薪泻邪

    for joke in jokes:
        choose_joke_button = types.KeyboardButton(text = str(jokes.index(joke)+1))
        jokesKeyboard.add(choose_joke_button)
        bot.send_audio(chat_id, open('jokes/' + joke["name"], 'rb'), performer = "CallPrankBot", title = joke["title"])
        #袨褌锌褉邪胁谢褟械屑 邪褍写懈芯 写芯褋褌褍锌薪褘褏 褉芯蟹褘谐褉褘褕械泄

    jokesKeyboard.add(back_button)
    return jokesKeyboard

users = []
#小锌懈褋芯泻 锌芯谢褜蟹芯胁邪褌械谢械泄

commandSet = ['start']
#袛芯褋褌褍锌薪褘械 泻芯屑邪薪写褘

back_button = types.KeyboardButton(text = "袧邪蟹邪写 鈫╋笍")
#袣薪芯锌泻邪 薪邪蟹邪写

mainKeyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
available_jokes_button = types.KeyboardButton(text = '袪芯蟹褘谐褉褘褕懈 馃コ')
#袨褋薪芯胁薪邪褟 泻谢邪胁懈邪褌褍褉邪
mainKeyboard.add(available_jokes_button)

backKeyboard = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
#袣谢邪胁懈邪褌褍褉邪 褋 泻薪芯锌泻芯泄 薪邪蟹邪写
backKeyboard.add(back_button)

def identification(id):
    user = None
    for u in users:
        if u["id"] == id:
            user = u
    #袩褉芯胁械褉褟械屑 锌芯谢褜蟹芯胁邪褌械谢褟 薪邪 薪邪褏芯卸写械薪懈械 胁 褋锌懈褋泻械 斜芯褌邪
    
    if user == None:
        #袧芯胁褘泄 锌芯谢褜蟹芯胁邪褌械谢褜
        newArray = {'id': id, "extensions": {"chosenButton": "", "prank_id": 0}}
        users.append(newArray)
        user = users[-1]
        
    return user

@bot.message_handler(commands=commandSet)
def send_welcome(message):
    user = identification(message.chat.id)
        
    if message.text in ("/start", "/help"):
        #袨褌锌褉邪胁谢褟械屑 锌褉懈胁械褌褋褌胁械薪薪芯械 褋芯芯斜褖械薪懈械 懈 泻谢邪胁懈邪褌褍褉褍
        bot.send_message(message.chat.id, hello_text, reply_markup = mainKeyboard)
        
@bot.message_handler(content_types=['text'])
def joking(message):
    user = identification(message.chat.id)
    
    if message.text == "袪芯蟹褘谐褉褘褕懈 馃コ":
        user["extensions"]["chosenButton"] = "袙褋械 褉芯蟹褘谐褉褘褕懈"
        jokesKeyboard = getJokesKeyboard(message.chat.id)
        bot.send_message(message.chat.id, "袙褘斜械褉懈褌械 锌褉邪薪泻 写谢褟 蟹胁芯薪泻邪", reply_markup = jokesKeyboard)
    
    elif user["extensions"]["chosenButton"] == "袙褋械 褉芯蟹褘谐褉褘褕懈":
        if message.text == "袧邪蟹邪写 鈫╋笍":
            user["extensions"]["chosenButton"] = ""
            bot.send_message(message.chat.id, "袙芯蟹胁褉邪褖邪褞...", reply_markup = mainKeyboard)
        else:
            try:
                prank_id = int(message.text)
                user["extensions"]["prank_id"] = prank_id
                user["extensions"]["chosenButton"] = "袙胁芯写 褌械谢械褎芯薪邪"
                bot.send_message(message.chat.id, "袙胁械写懈 薪芯屑械褉 褔械谢芯胁械泻邪, 泻芯褌芯褉芯屑褍 褏芯褔械褕褜 蟹邪泻邪蟹邪褌褜 蟹胁芯薪芯泻 胁 褎芯褉屑邪褌械 +7xxxxxxxxxx", reply_markup = backKeyboard)
            except Exception as e:
                pass
            
    elif user["extensions"]["chosenButton"] == "袙胁芯写 褌械谢械褎芯薪邪":
        if message.text == "袧邪蟹邪写 鈫╋笍":
            jokesKeyboard = getJokesKeyboard(message.chat.id)
            user["extensions"]["chosenButton"] = "袙褋械 褉芯蟹褘谐褉褘褕懈"
            bot.send_message(message.chat.id, "袙芯蟹胁褉邪褖邪褞...", reply_markup = jokesKeyboard)
        else:
            user["extensions"]["chosenButton"] = "袨锌谢邪褌邪 懈 蟹胁芯薪芯泻"
            phone = re.search("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message.text)
            #袩褉芯胁械褉褟械屑 褌械谢械褎芯薪 褋 锌芯屑芯褖褜褞 褉械谐褍谢褟褉薪芯谐芯 胁褘褉邪卸械薪懈褟
            if phone:
                with closing(pymysql.connect(host='localhost', user='root', password='', db='callprank', charset='utf8mb4', cursorclass=DictCursor)) as conn:
                    with conn.cursor() as cursor:
                        data = [(message.chat.id, message.text, 0, user["extensions"]["prank_id"], 0)]
                        query = 'INSERT INTO orders (chat_id, phone, isPaid, prank_id, done) VALUES (%s, %s, %s, %s, %s)'
                        cursor.executemany(query, data)
                        conn.commit()
                        
                        sql = ("SELECT * FROM orders ORDER BY id")
                        cursor.execute(sql)
                        orders = cursor.fetchall()
                payment_id = orders[-1]["id"]
                bot.send_message(message.chat.id, "袨锌谢邪褌懈褌械 蟹胁芯薪芯泻 芯写薪懈屑 泻谢懈泻芯屑: http://127.0.0.1/pay/%s" % payment_id, reply_markup = backKeyboard)
        
    elif user["extensions"]["chosenButton"] == "袨锌谢邪褌邪 懈 蟹胁芯薪芯泻":
        if message.text == "袧邪蟹邪写 鈫╋笍":
            user["extensions"]["chosenButton"] = "袙胁芯写 褌械谢械褎芯薪邪"
            bot.send_message(message.chat.id, "袙胁械写懈 薪芯屑械褉 褔械谢芯胁械泻邪, 泻芯褌芯褉芯屑褍 褏芯褔械褕褜 蟹邪泻邪蟹邪褌褜 蟹胁芯薪芯泻", reply_markup = backKeyboard)
        else:
            phone = re.search("^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$", message.text)
            #袩褉芯胁械褉褟械屑 褌械谢械褎芯薪 褋 锌芯屑芯褖褜褞 褉械谐褍谢褟褉薪芯谐芯 胁褘褉邪卸械薪懈褟
            undone_order = None
            if phone:
                with closing(pymysql.connect(host = "localhost", user = "root", password = "", db = "callprank", charset = "utf8mb4")) as conn:
                    with conn.cursor() as cursor:
                        query = ("SELECT * FROM orders WHERE done=0 AND isPaid=1 AND chat_id=%s") % message.chat.id
                        cursor.execute(query)
                        undone_orders = cursor.fetchall()
                #袩芯谢褍褔邪械屑 芯锌谢邪褔械薪薪褘械, 薪芯 薪械 胁褘锌芯谢薪械薪薪褘械 蟹邪泻邪蟹褘 锌芯谢褜蟹芯胁邪褌械谢褟
                
                if len(undone_orders) != 0:
                    undone_order = undone_orders[0]
                    call(undone_order["chat_id"], campaigns[undone_order["prank_id"]-1], undone_order["phone"], undone_order["id"])
                    #袛芯斜邪胁谢褟械屑 蟹胁芯薪芯泻 胁 芯褔械褉械写褜
                    
if __name__ == '__main__':
    bot.polling(none_stop = False, interval = 0, timeout = 20)