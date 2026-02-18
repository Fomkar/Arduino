# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 14:03:07 2026

@author: Fomkar
"""

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

arduino_port = find_arduino_port()

board = Arduino("115200", port=arduino_port)
board.LCD.init()            # LCD başlat
board.LCD.print_at(1, 0, "Öğretim Görevlisi")
board.LCD.print_at(4, 1, "Bunu")
board.LCD.print_at(0, 2, "Elektronik Otomasyon")
board.LCD.print_at(2, 3, "Yapay Zeka Prog.")



board.close()

