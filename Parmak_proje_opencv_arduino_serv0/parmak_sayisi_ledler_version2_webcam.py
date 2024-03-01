# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 10:54:38 2024

@author: Gitek_Micro
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 21:06:54 2024

@author: fomkar
"""


import cv2 
from cvzone.HandTrackingModule import HandDetector 
from Arduino import Arduino
import time

import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print ("Arduinonuz " +  p.name + " portuna bağlıdır.")

board = Arduino("9600", port=p.name) # plugged in via USB, serial com at rate 115200
led_dizi =[]
for i in range(8,13):
    print(i)
    board.pinMode(i, "OUTPUT")
    led_dizi.append(i)
detector = HandDetector(maxHands=1, detectionCon=0.8) 
video = cv2.VideoCapture(0) 

def led_yak(liste):
    for i in liste:
        print(i)
        board.digitalWrite(i,"HIGH")
        time.sleepqq(0.1)
  
while True: 
    _, img = video.read() 
    img = cv2.flip(img, 1) 
    hand = detector.findHands(img, draw=True) 
    fing = cv2.imread("0.jpg") 
    # board.digitalWrite(led_dizi[0], "LOW")
    # board.digitalWrite(led_dizi[1], "LOW")
    # board.digitalWrite(led_dizi[2], "LOW")
    # board.digitalWrite(led_dizi[3], "LOW")
    # board.digitalWrite(led_dizi[4], "LOW")
    # time.sleep(0.1)
    if len(hand[0]) > 0:
        if hand: 
            lmlist = hand[0][0]
            if lmlist: 
                fingerup = detector.fingersUp(lmlist) 
                fingerup[0]= int(not(fingerup[0]))
                print(fingerup)
                sayac = fingerup.count(1)
                # if fingerup[0] == 1:
                #     fing = cv2.imread("1.jpg")
                #     board.digitalWrite(led_dizi[0], "HIGH")
                #     # time.sleep(0.1)
                # if fingerup[1] == 1: 
                #     fing = cv2.imread("2.jpg")
                #     board.digitalWrite(led_dizi[1], "HIGH")
                #     # time.sleep(0.1)
                # if fingerup[2] == 1: 
                #     fing = cv2.imread("3.jpg")
                #     board.digitalWrite(led_dizi[2], "HIGH")
                #     # time.sleep(0.1)
                # if fingerup[3] == 1:
                #     fing = cv2.imread("4.jpg")
                #     board.digitalWrite(led_dizi[3], "HIGH")
                #     # time.sleep(0.1)
                # if fingerup[4] == 1: 
                #     fing = cv2.imread("5.jpg")
                #     # board.digitalWrite(led_dizi[4], "HIGH")
                # time.sleep(0.1)
                for i in range(len(fingerup)):
                  if fingerup[i] == 1:
                      print(sayac)
                      board.digitalWrite(led_dizi[i], "HIGH")
                      fing = cv2.imread(str(sayac)+".jpg")
                  elif fingerup[i] == 0:
                      board.digitalWrite(led_dizi[i], "LOW")
                time.sleep(0.001)
                # led.value(binary_list[i])   
    else:
        board.digitalWrite(led_dizi[0], "LOW")
        board.digitalWrite(led_dizi[1], "LOW")
        board.digitalWrite(led_dizi[2], "LOW")
        board.digitalWrite(led_dizi[3], "LOW")
        board.digitalWrite(led_dizi[4], "LOW")
        #     time.sleep(0.1)
    fing = cv2.resize(fing, (220, 280)) 
    img[50:330, 20:240] = fing 
    cv2.imshow("Video", img) 
      
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
board.close()
video.release() 
cv2.destroyAllWindows() 