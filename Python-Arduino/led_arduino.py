from Arduino import Arduino
import time

board = Arduino("9600", port="COM3") # plugged in via USB, serial com at rate 115200
board.pinMode(3, "OUTPUT")
board.pinMode(9, "OUTPUT")

board.pinMode(7, "INPUT")

while True:
    output = board.digitalRead(7)
    print(output)
    if output == 0:
        board.analogWrite(9, 255)
        time.sleep(0.1)
    else:
         board.analogWrite(9, 0)
         time.sleep(0.1)
