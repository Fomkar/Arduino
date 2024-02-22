# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 15:52:12 2024

@author: Gitek_Micro
"""


from machine import Pin
import utime

# Sıralı olarak 8 LED'i yakıp söndürme
led_pins = [Pin(i, Pin.OUT) for i in range(1, 9)] # GPIO pinlerini 2'den 9'a kadar kullan
for i in range(5): # 5 kez tekrarla
    for led in led_pins:
        led.value(1) # LED'i yak
        utime.sleep(0.5) # 0.5 saniye bekle
        led.value(0) # LED'i söndür
        utime.sleep(0.5) # 0.5 saniye bekle



"""
from machine import Pin
import time
led_pins = [Pin(i, Pin.OUT) for i in range(1, 9)] 


dizi = led_pins

while True:
    for i in range(0,len(dizi) -1, +1):
        print(i+1, ". led yandı.")
        dizi[i].high()
        time.sleep(0.5)
        dizi[i].low()

    for j in range(len(dizi) -1, 0, -1):
        print(j+1, ". led yandı.")
        dizi[j].high()
        time.sleep(0.5)
        dizi[j].low()

"""


"""

#%% Kullanıcıdan bir sayı girişi al
sayi = int(input("Lütfen bir sayı girin: "))

# Sayıyı ikili (binary) sistemine çevirme fonksiyonu
def DecimalToBinary(num):
    output=""
    while num >= 1:
        num = (num // 2)
        output = "{}{}".format(num % 2 , output)
    print(num % 2, end = '\n')
    return output

sonuc = str(DecimalToBinary(sayi))

bin_son = sonuc[::-1]

print("Girdiğiniz Sayı : ",sayi,"\nÇıkan Sonuc :",sonuc)
print("Sonucun Tersi : ",bin_son)


"""

from machine import Pin
import utime

# GPIO pinleri için LED dizisi
led_pins = [Pin(i, Pin.OUT) for i in range(1, 9)]

# Kullanıcıdan bir sayı girişi al
sayi = int(input("Lütfen bir sayı girin: "))

# Sayıyı ikili (binary) sistemine çevirme fonksiyonu
def DecimalToBinary(num):
    output=""
    while num > 0:
        num = (num // 2)
        output = "{}{}".format(num % 2 , output)
    print(num % 2, end = '\n')
    return output + str(1)



# Gelen ikili değeri LED'lere göre ayarlama
def control_leds(binary):
    # LED'leri sıfırla
    for led in led_pins:
        led.off()


    binary = list(reversed(binary))

    # LED'leri kontrol et
    for i in range(len(binary)):
        if binary[i] == '1':
            led_pins[i].on()

# Sayıyı ikili forma çevir
binary_num = str(DecimalToBinary(sayi))

print("Binary Sayi : ",binary_num, end = '\n')
# LED'leri kontrol et
control_leds(binary_num)





