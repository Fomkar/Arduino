# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 19:59:55 2024

@author: fomkar
"""
#%% Led Yakma
from Arduino import Arduino
import time

board = Arduino("9600", port="COM3") # plugged in via USB, serial com at rate 115200
board.pinMode(13, "OUTPUT")
board.pinMode(6, "OUTPUT")

while True:
   
    board.digitalWrite(13, "HIGH")
    board.analogWrite(6, 0)
    time.sleep(1)

    board.digitalWrite(13, "LOW")
    board.analogWrite(6, 45)
    time.sleep(1)
    veri = input("deger giriniz :")
    if veri == "q":
        break
board.close()

#%%Servo motor

from Arduino import Arduino
import time

board = Arduino("9600", port="COM3") # plugged in via USB, serial com at rate 115200
board.pinMode(13, "OUTPUT")
board.pinMode(6, "OUTPUT")
servo_pin = 6
board.Servos.attach(servo_pin)


def move_servo(angle):
    board.Servos.write(servo_pin, angle)

# Servo motoru belirli bir açıda döndürmek için örnek bir çağrı

while True:
   
    board.digitalWrite(13, "HIGH")
    move_servo(45)  # Servo motoru 90 dereceye döndür
    time.sleep(1)

    board.digitalWrite(13, "LOW")
    move_servo(0)  # Servo motoru 90 dereceye döndür
    time.sleep(1)
    veri = input("deger giriniz :")
    if veri == "q":
        break
board.close()

#%%Servo motor 2 tane

from Arduino import Arduino
import time

board = Arduino("9600", port="COM6") # plugged in via USB, serial com at rate 115200
board.pinMode(13, "OUTPUT")
board.pinMode(6, "OUTPUT")
servo_pin = 6
servo_pin_1 = 5
board.Servos.attach(servo_pin)
board.Servos.attach(servo_pin_1)

def move_servo(servo_pin,angle):
    board.Servos.write(servo_pin, angle)

# Servo motoru belirli bir açıda döndürmek için örnek bir çağrı

while True:
   
    board.digitalWrite(13, "HIGH")
    move_servo(6,45)  # Servo motoru 90 dereceye döndür
    move_servo(5,0)
    time.sleep(0.5)

    board.digitalWrite(13, "LOW")
    move_servo(6,0)  # Servo motoru 90 dereceye döndür
    move_servo(5,45)  # Servo motoru 90 dereceye döndür
    time.sleep(0.5)
    veri = input("deger giriniz :")
    if veri == "q":
        break
board.close()

