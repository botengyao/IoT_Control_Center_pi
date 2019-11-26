import sys
import faceidentifier
import temphumidity
import dashboard
import getlight
import glo
import RPi.GPIO as GPIO
import subprocess
import time, threading

import pygame
from pygame.locals import *
import os
from collections import deque

import board
import adafruit_dht
LDR = board.D13
level = 0
'''
class status:
    def __init__(self, temp, humid, light):
        self.temp = 0
        self.humid = 0
        self.light = 0
        self.start_system = False
        self.auto_start = True
        self.code_run = True
'''

#os.putenv('SDL_VIDEODRIVER', 'fbcon')
#os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(5, GPIO.OUT)

glo.hum = GPIO.PWM(5, 10)
glo.hum.start(50)

start_time = time.time()

dhtDevice = adafruit_dht.DHT11(board.D19)

pygame.init()
pygame.mouse.set_visible(False)

window_size = (width, height) = (320, 240)
WHITE = 255, 255, 255
BLACK = 0,0,0
screen = pygame.display.set_mode(window_size)
my_font = pygame.font.Font(None, 22)

start_face = {'Start face recorgnization':(120,120)}
iot_system = {'Iot system 1.0' :(120,120)}
please_retry = {'Please retry':(120,120)}
welcome = {'welcome to back home':(120,120)}
temp_humid = ["temperature: ", "humidility: "]
position = [(120, 80), (120, 160)]

s_per_sec = 10
fps_clock = pygame.time.Clock()

def start_fact_recog(channel):
    global level
    level = 1
    if faceidentifier.start_face_detection():
        level = 2
    else:
        level = 3

def quit_whole(channel):
    glo.code_run = False

def dash_board():
    dashboard.dash_board(GPIO)

def get_value():
    while glo.code_run:
        temp1 = temphumidity.getTempOrHumid(dhtDevice,"temp")
        humid1 = temphumidity.getTempOrHumid(dhtDevice,"humid")
        if temp1 and humid1:
            glo.temp = temp1
            glo.humid = humid1
        glo.light = getlight.getLight()
        time.sleep(5)

GPIO.add_event_detect(17, GPIO.FALLING,callback=start_fact_recog, bouncetime=300)
GPIO.add_event_detect(27, GPIO.FALLING,callback=quit_whole, bouncetime=300)

t_temp = threading.Thread(target=get_value, name='get_temp')
t_temp.start()

t_dashboard = threading.Thread(target=dash_board, name='dashboard')
t_dashboard.start()

while glo.code_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            glo.code_run = False # Here we exit the Loop and execute what after.
            
    if level == 0:
        screen.fill(WHITE) 
        for my_text, text_pos in iot_system.items():
            text_surface = my_font.render(my_text, True, BLACK)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)

        pygame.display.flip()
        time.sleep(1)
        level = 4

    if level == 1:
        screen.fill(WHITE) 
        for my_text, text_pos in start_face.items():
            text_surface = my_font.render(my_text, True, BLACK)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)

    if level == 2:
        #GPIO.output(26, GPIO.HIGH)
        screen.fill(WHITE) 
        for my_text, text_pos in welcome.items():
            text_surface = my_font.render(my_text, True, BLACK)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
        time.sleep(1)
        #GPIO.output(26, GPIO.LOW)
        level = 4
    
    if level == 3:
        screen.fill(WHITE) 
        for my_text, text_pos in please_retry.items():
            text_surface = my_font.render(my_text, True, BLACK)
            rect = text_surface.get_rect(center=text_pos)
            screen.blit(text_surface, rect)
        time.sleep(1)
        level = 0

    if level == 4:
        #print(temp)
        #print(humid)
        temp_humid[0] = "Temperature: " + str(glo.temp)
        temp_humid[1] = "Humidity: " + str(glo.humid) 
        screen.fill(WHITE)
        for i in range(len(temp_humid)):
            text_surface = my_font.render(temp_humid[i], True, BLACK)
            rect = text_surface.get_rect(center=position[i])
            screen.blit(text_surface, rect)

    pygame.display.flip()
    pygame.display.update()
    fps_clock.tick(s_per_sec)

GPIO.cleanup()
#GPIO.cleanup()
pygame.quit()
#t_dashboard.join()  
#t_temp.join()  
