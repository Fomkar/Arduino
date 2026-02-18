# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:03:33 2026

@author: Fomkar
"""

from Arduino import Arduino
import time
import serial.tools.list_ports

def find_arduino_port():
    """Arduino'nun bağlı olduğu portu otomatik olarak bulur."""
    ports = serial.tools.list_ports.comports()
    
    # Arduino'lar genellikle bu anahtar kelimeleri içerir
    arduino_keywords = ["Arduino", "CH340", "CH341", "FTDI", "USB Serial", "USB-SERIAL", "ACM", "usbserial"]
    
    for port in ports:
        description = (port.description or "").upper()
        manufacturer = (port.manufacturer or "").upper()
        
        for keyword in arduino_keywords:
            if keyword.upper() in description or keyword.upper() in manufacturer:
                print(f"Arduino bulundu: {port.device} ({port.description})")
                return port.device
    
    # Bulunamazsa mevcut portları listele
    print("Arduino otomatik bulunamadı. Mevcut portlar:")
    for port in ports:
        print(f"  {port.device} - {port.description}")
    
    raise Exception("Arduino bağlı değil veya tanınamadı!")

# Otomatik port bul
arduino_port = find_arduino_port()

board = Arduino("115200", port=arduino_port)
board.pinMode(13, "OUTPUT")
board.Servos.attach(9)

i = 10
while i > 0:
    board.digitalWrite(13, "HIGH")
    time.sleep(0.2)
    board.digitalWrite(13, "LOW")
    time.sleep(0.3)
    i = i - 1

board.close()