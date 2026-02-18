"""
Arduino LCD I2C — Python Sürücüsü
===================================
prototype.ino (V0.7) ile çalışır.
LCD komutları Serial üzerinden gönderilir.

Komut Tablosu:
  lci%<cols>%<rows>%0$!   → LCD başlat
  lcb%<0|1>$!             → Arka ışık (1=açık, 0=kapalı)
  lcc%$!                  → Ekranı temizle
  lch%$!                  → İmleci home'a al
  lcs%<col>%<row>$!       → setCursor
  lcp%<text>$!            → Mevcut konuma yaz
  lcsp%<col>%<row>%<text>$! → setCursor + print (tek komut)
"""

from Arduino import Arduino
import serial.tools.list_ports
import time


# ─────────────────────────────────────────────
#  Otomatik Port Bulma
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
#  LCD Sınıfı
# ─────────────────────────────────────────────

class LCD:
    """
    Arduino üzerindeki I2C LCD ekranı Python'dan yönetir.

    Kullanım:
        lcd = LCD(board, cols=20, rows=4, address=0x27)
        lcd.init()
        lcd.set_cursor(0, 0)
        lcd.print("Merhaba!")
    """

    def __init__(self, board: Arduino, cols: int = 20, rows: int = 4, address: int = 0x27):
        self.board   = board
        self.cols    = cols
        self.rows    = rows
        self.address = address  # şu an ino tarafında sabit; ileride dinamik yapılabilir

    def _send(self, cmd: str, data: str = "") -> str:
        """Ham Serial komut gönderir, Arduino'nun yanıtını okur."""
        # Arduino kütüphanesi board.SoftwareSerial üzerinden değil,
        # doğrudan board.sp (serial port) üzerinden yazıyoruz.
        message = f"%{cmd}%{data}$!"
        self.board.sp.write(message.encode())
        time.sleep(0.05)
        response = self.board.sp.readline().decode("utf-8", errors="ignore").strip()
        return response

    def init(self):
        """LCD'yi başlatır ve arka ışığı açar."""
        resp = self._send("lci", f"{self.cols}%{self.rows}%0")
        print(f"LCD init → {resp}")

    def backlight(self, on: bool = True):
        """Arka ışığı açar veya kapatır."""
        self._send("lcb", "1" if on else "0")

    def clear(self):
        """Ekranı temizler."""
        self._send("lcc", "")

    def home(self):
        """İmleci sol üst köşeye (0,0) taşır."""
        self._send("lch", "")

    def set_cursor(self, col: int, row: int):
        """İmleci belirtilen konuma taşır. col: sütun (0‑19), row: satır (0‑3)"""
        self._send("lcs", f"{col}%{row}")

    def print(self, text: str):
        """İmleç bulunduğu konumdan itibaren metin yazar."""
        self._send("lcp", text)

    def print_at(self, col: int, row: int, text: str):
        """Belirtilen konuma gidip metin yazar (tek komut)."""
        self._send("lcsp", f"{col}%{row}%{text}")

    def display_lines(self, lines: list):
        """
        Her satır için (col, row, text) içeren liste alır.
        Örnek: [(1,0,"Başlık"), (0,1,"Alt satır")]
        """
        self.clear()
        for col, row, text in lines:
            self.print_at(col, row, text)


# ─────────────────────────────────────────────
#  Ana Program
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # 1) Arduino'ya bağlan
    arduino_port = find_arduino_port()
    board = Arduino("115200", port=arduino_port)

    # 2) LCD nesnesini oluştur (20x4 ekran, I2C adres 0x27)
    lcd = LCD(board, cols=20, rows=4, address=0x27)

    # 3) LCD'yi başlat
    lcd.init()
    time.sleep(0.5)

    # 4) C++ örneğindeki içerik — aynısı Python'dan:
    lcd.display_lines([
        (1, 0, "Öğretim Görevlisi"),
        (4, 1, "Ömer Karagöz"),
        (0, 2, "Elektronik Otomasyon"),
        (2, 3, "Yapay Zeka Prog."),
    ])

    print("LCD yazıldı! 5 saniye bekleniyor...")
    time.sleep(5)

    # 5) Ekranı temizle ve bağlantıyı kapat
    lcd.clear()
    board.close()
    print("Bağlantı kapatıldı.")
