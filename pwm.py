#!/usr/bin/env python
# coding: utf-8

import RPi.GPIO as GPIO
import sys
import subprocess
import time
import warnings
import threading
import datetime

SW_PORT = 4
LED_R_PORT = 13
LED_G_PORT = 19
LED_B_PORT = 26
DELAY = 0.02

def get_temp_humi():
    temp = "Failed to get temperature"
    humi = 50.0
    while True:
        for t in open('/proc/usbrh/0/temperature', 'r'):
            temp = t.replace('\n','')
        for h in open('/proc/usbrh/0/humidity', 'r'):
            humi = h.replace('\n','')
        if "." in temp:
            break
#       print "Error " + temp
        time.sleep(1)

    temp = float(temp)
    humi = float(humi)
    huka = 0.81 * temp + 0.01 * humi * (0.99 * temp -14.3) + 46.3
    temp = round(temp,1)
    humi = round(humi,1)

    day = datetime.datetime.now()
    d = str(day.hour) + '時' + str(day.minute) + '分'
    text = d + 'です。今の温度は' + str(temp) + '度です。湿度は' + str(humi) + '％なので、'
    text = text + '不快指数は' + str(int(huka)) + 'です。つまり、'
    if huka < 55 :
        text = text + '教室は寒すぎます。耐えられません。'
    elif huka < 60 :
        text = text + '教室は肌寒いです。'
    elif huka < 65 :
        text = text + '教室の環境は特に問題ありません。'
    elif huka < 70 :
        text = text + '教室は快いです。'
    elif huka < 75 :
        text = text + '教室は暑くありません。'
    elif huka < 80 :
        text = text + '教室はやや暑いです。'
    elif huka < 85 :
        text = text + '教室は暑くて汗が出るほど不快です。'
    else:
        text = text + '教室は暑すぎます。耐えられません。'
    return text



class Led():

    def __init__(self):
        self.stop_event = threading.Event()
        self.thread_led = threading.Thread(target=self.gradation, args=())
        self.thread_led.start()

    def kill_check(self):
        if self.stop_event.is_set():
            return True
        time.sleep(DELAY)
        return False

    def led_R_G(self):
        self.pwmR.start(0)
        self.pwmG.start(100)
        self.pwmB.start(100)
        for i in range(1, 101):
            self.pwmR.start(i)
            self.pwmG.start(100-i)
            if self.kill_check():
                return False
        return True
    def led_G_B(self):
        self.pwmR.start(100)
        self.pwmG.start(0)
        self.pwmB.start(100)
        for i in range(1, 101):
            self.pwmG.start(i)
            self.pwmB.start(100-i)
            if self.kill_check():
                return False
        return True
    def led_B_R(self):
        self.pwmR.start(100)
        self.pwmG.start(100)
        self.pwmB.start(0)
        for i in range(1, 101):
            self.pwmB.start(i)
            self.pwmR.start(100-i)
            if self.kill_check():
                return False
        return True
    def gradation(self):
        print "---Start Thread"
        self.pwmR = GPIO.PWM(LED_R_PORT, 1000)
        self.pwmG = GPIO.PWM(LED_G_PORT, 1000)
        self.pwmB = GPIO.PWM(LED_B_PORT, 1000)

        while True:
            if not self.led_R_G():
                break
            if not self.led_G_B():
                break
            if not self.led_B_R():
                break

        self.pwmR.stop()
        self.pwmG.stop()
        self.pwmB.stop()
        print "---Finish Thread"

    def stop(self):
        self.stop_event.set()
        self.thread_led.join()

if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SW_PORT, GPIO.IN)
    GPIO.setup(LED_R_PORT, GPIO.OUT)
    GPIO.setup(LED_G_PORT, GPIO.OUT)
    GPIO.setup(LED_B_PORT, GPIO.OUT)
    
    value = -1 # チャタリング対策

    try:
        led = Led()
        while True:
            GPIO.wait_for_edge(SW_PORT, GPIO.BOTH)
            time.sleep(0.1)
            if GPIO.input(SW_PORT) != value:
        #        print "Change!"
                led.stop()
                GPIO.output(LED_R_PORT, GPIO.HIGH)
                GPIO.output(LED_G_PORT, GPIO.HIGH)
                GPIO.output(LED_B_PORT, GPIO.LOW)
                value = GPIO.input(SW_PORT)
                text = get_temp_humi()
                GPIO.output(LED_R_PORT, GPIO.HIGH)
                GPIO.output(LED_G_PORT, GPIO.LOW)
                GPIO.output(LED_B_PORT, GPIO.HIGH)
                curl = "curl \"https://api.voicetext.jp/v1/tts\" -o \"test.wav\" -u \"xxxx:xxxx\" -d \"text=" + text + "\" -d \"speaker=haruka\" -d \"pitch=140\" -d \"emotion=happiness\" -d \"emotion_level=3\" -d \"volume=200\""
    #            subprocess.check_call(curl.split(" "))
                subprocess.check_call(curl, shell=True)
                GPIO.output(LED_R_PORT, GPIO.LOW)
                GPIO.output(LED_G_PORT, GPIO.HIGH)
                GPIO.output(LED_B_PORT, GPIO.HIGH)
                subprocess.check_call(["aplay", "test.wav"])
                led = Led()
    except KeyboardInterrupt:
        print("W: interrupt received, stopping…")
    finally:
        led.stop()
        GPIO.cleanup()

sys.exit(0)

