# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 13:25:58 2026

@author: Fomkar
"""

from Arduino import Arduino
import time

board = Arduino("115200", port="COM7") #Windows example
board.pinMode(13, "OUTPUT")
board.Servos.attach(9) #declare servo on pin 9
i= 5
while i > 0 :
    board.digitalWrite(13, "LOW")
    time.sleep(1)
    board.digitalWrite(13, "HIGH")
    time.sleep(1)
    i = i - 1
    
    board.Servos.write(9, 0) #move servo on pin 9 to 0 degrees
    print (board.Servos.read(9)) # should be 0
    time.sleep(1)
    board.Servos.write(9, 90) #move servo on pin 9 to 0 degrees
    print (board.Servos.read(9)) # should be 0
    time.sleep(1)
    board.Servos.write(9, 180) #move servo on pin 9 to 0 degrees
    print (board.Servos.read(9)) # should be 0
    time.sleep(1)
    board.Servos.write(9, 90) #move servo on pin 9 to 0 degrees
    print (board.Servos.read(9)) # should be 0
    time.sleep(1)

board.close()
