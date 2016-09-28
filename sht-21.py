#!/usr/bin/env python
# coding: utf-8

from requests_oauthlib import OAuth1Session

import time
import datetime
import sys

temp = "Failed to get temperature"
humi = 50.0
while True:
    for t in open('/proc/usbrh/0/temperature', 'r'):
        temp = t.replace('\n','')
    for h in open('/proc/usbrh/0/humidity', 'r'):
        humi = h.replace('\n','')
    if "." in temp:
        break
#    print "Error " + temp
    time.sleep(1)

temp = float(temp)
humi = float(humi)
huka = 0.81 * temp + 0.01 * humi * (0.99 * temp -14.3) + 46.3
temp = round(temp,1)
humi = round(humi,1)

day = datetime.datetime.now()
d = str(day.year) + '年' + str(day.month) + '月' + str(day.day) + '日' + str(day.hour) + '時' + str(day.minute) + '分'
text = d + '現在、岩田研の室温は' + str(temp) + '度です。湿度は' + str(humi) + '％なので、'
text = text + '不快指数は' + str(int(huka)) + 'です。つまり、'
if huka < 55 :
    text = text + '岩田研は寒すぎます。耐えられません。'
elif huka < 60 :
    text = text + '岩田研は肌寒いです。'
elif huka < 65 :
    text = text + '岩田研の環境は特に問題ありません。'
elif huka < 70 :
    text = text + '岩田研は快いです。'
elif huka < 75 :
    text = text + '岩田研は暑くありません。'
elif huka < 80 :
    text = text + '岩田研はやや暑いです。'
elif huka < 85 :
    text = text + '岩田研は暑くて汗が出るほど不快です。'
else:
    text = text + '岩田研は暑すぎます。耐えられません。'

#print "%s" % text
#sys.exit()

CK = 'xxxxxxxxxxxxxxxxxxxxxxxxx'                          # Consumer Key
CS = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Consumer Secret
AT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # Access Token
AS = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'      # Accesss Token Secert

# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update.json"

# ツイート本文
params = {"status": text}

# OAuth認証で POST method で投稿
twitter = OAuth1Session(CK, CS, AT, AS)
req = twitter.post(url, params = params)

# レスポンスを確認
#if req.status_code == 200:
#    print ("OK")
#else:
#    print ("Error: %d" % req.status_code)


