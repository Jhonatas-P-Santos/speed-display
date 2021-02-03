# Dependências Externas
import RPi.GPIO as gpio
import tm1637

import time
import re
import subprocess
import math
import threading as th

# Portas GPIO ( altere para as portas que você está usando )
buttonPort = 26 # Porta GPIO que está conectado o botão
clkPort = 5 # Porta GPIO que está conectado o pino CLK do Display
dioPort = 4 # Porta GPIO que está conectado o pino DIO do Display

gpio.setmode(gpio.BCM)
gpio.setup(buttonPort, gpio.IN, gpio.PUD_UP)
tm = tm1637.TM1637(clk=clkPort, dio=dioPort)

def turnOffDisplay():
    tm.write([0, 0, 0, 0])
    
def inProgress():
    while (testing == True):
        tm.scroll('testando velocidade', delay=125)

def speedTest():
    print('Iniciando teste...')
    global testing
    testing = True

    th.Thread(target=inProgress).start()
    response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
    download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
    download = download.group(1)
        
    if (download):
        testing = False
        time.sleep(3)
        print('Velocidade de Download: ', download)
        downloadInt = float(download)
        downloadToDisplay = math.ceil(downloadInt)
        tm.show(str(downloadToDisplay))
        
    time.sleep(10)
    turnOffDisplay()
    print('Teste finalizado!')
    
while True:
    if gpio.input(26) == gpio.LOW:
        speedTest()