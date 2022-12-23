# -*- coding: utf-8 -*-
from Arduino import Arduino
import time

board = Arduino("9600", port="COM7") # plugged in via USB, serial com at rate 115200
board.pinMode(3, "OUTPUT")
i = 255
# while i > 199:
#     board.analogWrite(3, i)
#     print("deger : ",i)
#     time.sleep(5)
#     i -= 5
print("deger : 220")
board.analogWrite(3, 220)
time.sleep(2)

print("deger : 155")
board.analogWrite(3, 155)
time.sleep(2)

print("deger : 90")
board.analogWrite(3, 100)
time.sleep(2)


print("deger : 70")
board.analogWrite(3, 70)
time.sleep(2)

print("deger : 30")
board.analogWrite(3, 30)
time.sleep(2)

print("bitti !")
board.analogWrite(3, 0)
time.sleep(2)
board.close()
            # print("63")
            # board.analogWrite(3, i)
            # time.sleep(5)
            # print("68")
            # board.analogWrite(3, 68)
            # time.sleep(5)
            # print("73")
            # board.analogWrite(3, 73)
            # time.sleep(5)
