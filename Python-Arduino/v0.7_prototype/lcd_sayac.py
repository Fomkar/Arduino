from Arduino import Arduino
import serial.tools.list_ports
import time


def find_arduino_port():
    """Arduino'nun bağlı olduğu COM portunu otomatik bulur."""
    ports = serial.tools.list_ports.comports()
    arduino_keywords = ["Arduino", "CH340", "CH341", "FTDI",
                        "USB Serial", "USB-SERIAL", "ACM", "usbserial", "CP210"]

    for port in ports:
        description  = (port.description  or "").upper()
        manufacturer = (port.manufacturer or "").upper()
        for kw in arduino_keywords:
            if kw.upper() in description or kw.upper() in manufacturer:
                print(f"✓ Arduino bulundu: {port.device}  ({port.description})")
                return port.device

    print("⚠ Arduino otomatik bulunamadı. Mevcut portlar:")
    for port in ports:
        print(f"   {port.device}  →  {port.description}")
    raise Exception("Arduino bağlı değil veya tanınamadı!")


# ── Bağlantı ──────────────────────────────────────────
arduino_port = find_arduino_port()
board = Arduino("115200", port=arduino_port)

# ── LCD Başlat ────────────────────────────────────────
board.LCD.init()        # 20x4 ekran, backlight açık
time.sleep(0.5)

# ── Başlık satırı (sabit kalır) ───────────────────────
board.LCD.print_at(4, 0, "-- SAYAç --")
board.LCD.print_at(2, 3, "1'den 100'e kadar")

# ── 1'den 100'e say ───────────────────────────────────
for sayi in range(1, 10):

    # Sayıyı ortala (20 sütunlu ekranda)
    metin = str(sayi)
    col   = (20 - len(metin)) // 2   # yatay ortalama

    board.LCD.print_at(0,  1, "                    ")   # satırı temizle
    board.LCD.print_at(col, 1, metin)

    print(f"LCD → {sayi}")
    time.sleep(0.3)     # her sayı arasında 300ms bekle

# ── Bitti mesajı ──────────────────────────────────────

board.LCD.clear()
time.sleep(1)
board.LCD.print_at(3, 1, "Sayma Tamamlandi!")
board.LCD.print_at(3, 2, "Ekran temizlendi")
time.sleep(3)

# ── Ekranı temizle ve kapat ───────────────────────────
board.LCD.clear()
board.LCD.backlight(False)
board.close()
print("Bitti. Bağlantı kapatıldı.")
