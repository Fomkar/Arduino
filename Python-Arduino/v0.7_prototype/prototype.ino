#include <SoftwareSerial.h>
#include <Wire.h>
#include <Servo.h>
#include <EEPROM.h>
#include <LiquidCrystalTr_I2C.h>

void Version(){
  Serial.println(F("V0.7"));
}

SoftwareSerial *sserial = NULL;
Servo servos[8];
int servo_pins[] = {0, 0, 0, 0, 0, 0, 0, 0};
boolean connected = false;

// LCD nesnesi — adres, sütun, satır
LiquidCrystal_I2C lcd(0x27, 20, 4);
boolean lcd_initialized = false;

int Str2int (String Str_value)
{
  char buffer[10];
  Str_value.toCharArray(buffer, 10);
  int int_value = atoi(buffer);
  return int_value;
}

void split(String results[], int len, String input, char spChar) {
  String temp = input;
  for (int i=0; i<len; i++) {
    int idx = temp.indexOf(spChar);
    results[i] = temp.substring(0,idx);
    temp = temp.substring(idx+1);
  }
}

// ─────────────────────────────────────────────
//  LCD Komut İşleyicileri
// ─────────────────────────────────────────────

// lci%<cols>%<rows>%<addr>$!  → LCD başlat
void LCD_init(String data) {
  String sdata[3];
  split(sdata, 3, data, '%');
  int cols = sdata[0].length() > 0 ? Str2int(sdata[0]) : 20;
  int rows = sdata[1].length() > 0 ? Str2int(sdata[1]) : 4;
  // addr şu an sabit 0x27; ileride dinamik yapılabilir
  lcd = LiquidCrystal_I2C(0x27, cols, rows);
  lcd.begin();
  lcd.backlight();
  lcd_initialized = true;
  Serial.println("lc OK");
}

// lcb%<0|1>$!  → Arka ışık aç/kapat
void LCD_backlight(String data) {
  int val = Str2int(data);
  if (val) lcd.backlight();
  else     lcd.noBacklight();
  Serial.println("lc OK");
}

// lcc$!  → Ekranı temizle
void LCD_clear(String data) {
  lcd.clear();
  Serial.println("lc OK");
}

// lch$!  → Home konuma git
void LCD_home(String data) {
  lcd.home();
  Serial.println("lc OK");
}

// lcs%<col>%<row>$!  → setCursor
void LCD_setCursor(String data) {
  String sdata[2];
  split(sdata, 2, data, '%');
  int col = Str2int(sdata[0]);
  int row = Str2int(sdata[1]);
  lcd.setCursor(col, row);
  Serial.println("lc OK");
}

// lcp%<text>$!  → print
void LCD_print(String data) {
  lcd.print(data);
  Serial.println("lc OK");
}

// lcsc%<col>%<row>%<text>$!  → setCursor + print (tek seferde)
void LCD_setCursorPrint(String data) {
  int idx1 = data.indexOf('%');
  int idx2 = data.indexOf('%', idx1 + 1);
  int col  = Str2int(data.substring(0, idx1));
  int row  = Str2int(data.substring(idx1 + 1, idx2));
  String text = data.substring(idx2 + 1);
  lcd.setCursor(col, row);
  lcd.print(text);
  Serial.println("lc OK");
}

// ─────────────────────────────────────────────
//  Mevcut işleyiciler (değiştirilmedi)
// ─────────────────────────────────────────────

uint8_t readCapacitivePin(String data) {
  int pinToMeasure = Str2int(data);
  volatile uint8_t* port;
  volatile uint8_t* ddr;
  volatile uint8_t* pin;
  byte bitmask;
  port = portOutputRegister(digitalPinToPort(pinToMeasure));
  ddr = portModeRegister(digitalPinToPort(pinToMeasure));
  bitmask = digitalPinToBitMask(pinToMeasure);
  pin = portInputRegister(digitalPinToPort(pinToMeasure));
  *port &= ~(bitmask);
  *ddr  |= bitmask;
  delay(1);
  *ddr &= ~(bitmask);
  *port |= bitmask;
  uint8_t cycles = 17;
       if (*pin & bitmask) { cycles =  0;}
  else if (*pin & bitmask) { cycles =  1;}
  else if (*pin & bitmask) { cycles =  2;}
  else if (*pin & bitmask) { cycles =  3;}
  else if (*pin & bitmask) { cycles =  4;}
  else if (*pin & bitmask) { cycles =  5;}
  else if (*pin & bitmask) { cycles =  6;}
  else if (*pin & bitmask) { cycles =  7;}
  else if (*pin & bitmask) { cycles =  8;}
  else if (*pin & bitmask) { cycles =  9;}
  else if (*pin & bitmask) { cycles = 10;}
  else if (*pin & bitmask) { cycles = 11;}
  else if (*pin & bitmask) { cycles = 12;}
  else if (*pin & bitmask) { cycles = 13;}
  else if (*pin & bitmask) { cycles = 14;}
  else if (*pin & bitmask) { cycles = 15;}
  else if (*pin & bitmask) { cycles = 16;}
  *port &= ~(bitmask);
  *ddr  |= bitmask;
  Serial.println(cycles);
}

void Tone(String data){
  int idx = data.indexOf('%');
  int len = Str2int(data.substring(0,idx));
  String data2 = data.substring(idx+1);
  int idx2 = data2.indexOf('%');
  int pin = Str2int(data2.substring(0,idx2));
  String data3 = data2.substring(idx2+1);
  String melody[len*2];
  split(melody,len*2,data3,'%');
  for (int thisNote = 0; thisNote < len; thisNote++) {
    int noteDuration = 1000/Str2int(melody[thisNote+len]);
    int note = Str2int(melody[thisNote]);
    tone(pin, note, noteDuration);
    int pause = noteDuration * 1.30;
    delay(pause);
    noTone(pin);
  }
}

void ToneNo(String data){
  int pin = Str2int(data);
  noTone(pin);
}

void DigitalHandler(int mode, String data){
    int pin = Str2int(data);
    if(mode<=0){
        Serial.println(digitalRead(pin));
    }else{
        if(pin <0){
            digitalWrite(-pin,LOW);
        }else{
            digitalWrite(pin,HIGH);
        }
    }
}

void AnalogHandler(int mode, String data){
     if(mode<=0){
        int pin = Str2int(data);
        Serial.println(analogRead(pin));
    }else{
        String sdata[2];
        split(sdata,2,data,'%');
        int pin = Str2int(sdata[0]);
        int pv = Str2int(sdata[1]);
        analogWrite(pin,pv);
    }
}

void ConfigurePinHandler(String data){
    int pin = Str2int(data);
    if(pin <=0){
        pinMode(-pin,INPUT);
    }else{
        pinMode(pin,OUTPUT);
    }
}

void shiftOutHandler(String data) {
    String sdata[4];
    split(sdata, 4, data, '%');
    int dataPin = sdata[0].toInt();
    int clockPin = sdata[1].toInt();
    String bitOrderName = sdata[2];
    byte value = (byte)(sdata[3].toInt());
    if (bitOrderName == "MSBFIRST") {
       shiftOut(dataPin, clockPin, MSBFIRST, value);
    } else {
       shiftOut(dataPin, clockPin, LSBFIRST, value);
    }
}

void shiftInHandler(String data) {
    String sdata[3];
    split(sdata, 3, data, '%');
    int dataPin = sdata[0].toInt();
    int clockPin = sdata[1].toInt();
    String bitOrderName = sdata[2];
    int incoming;
    if (bitOrderName == "MSBFIRST") {
       incoming = (int)shiftIn(dataPin, clockPin, MSBFIRST);
    } else {
       incoming = (int)shiftIn(dataPin, clockPin, LSBFIRST);
    }
    Serial.println(incoming);
}

void SS_set(String data){
  delete sserial;
  String sdata[3];
  split(sdata,3,data,'%');
  int rx_ = Str2int(sdata[0]);
  int tx_ = Str2int(sdata[1]);
  int baud_ = Str2int(sdata[2]);
  sserial = new SoftwareSerial(rx_, tx_);
  sserial->begin(baud_);
  Serial.println("ss OK");
}

void SS_write(String data) {
 int len = data.length()+1;
 char buffer[len];
 data.toCharArray(buffer,len);
 Serial.println("ss OK");
 sserial->write(buffer);
}

void SS_read(String data) {
 char c = sserial->read();
 Serial.println(c);
}

void pulseInHandler(String data){
    int pin = Str2int(data);
    long duration;
    if(pin <=0){
          pinMode(-pin, INPUT);
          duration = pulseIn(-pin, LOW);
    }else{
          pinMode(pin, INPUT);
          duration = pulseIn(pin, HIGH);
    }
    Serial.println(duration);
}

void pulseInSHandler(String data){
    int pin = Str2int(data);
    long duration;
    if(pin <=0){
          pinMode(-pin, OUTPUT);
          digitalWrite(-pin, HIGH);
          delayMicroseconds(2);
          digitalWrite(-pin, LOW);
          delayMicroseconds(5);
          digitalWrite(-pin, HIGH);
          pinMode(-pin, INPUT);
          duration = pulseIn(-pin, LOW);
    }else{
          pinMode(pin, OUTPUT);
          digitalWrite(pin, LOW);
          delayMicroseconds(2);
          digitalWrite(pin, HIGH);
          delayMicroseconds(5);
          digitalWrite(pin, LOW);
          pinMode(pin, INPUT);
          duration = pulseIn(pin, HIGH);
    }
    Serial.println(duration);
}

void SV_add(String data) {
    String sdata[3];
    split(sdata,3,data,'%');
    int pin = Str2int(sdata[0]);
    int min = Str2int(sdata[1]);
    int max = Str2int(sdata[2]);
    int pos = -1;
    for (int i = 0; i<8;i++) {
        if (servo_pins[i] == pin) {
            servos[pos].detach();
            servos[pos].attach(pin, min, max);
            servo_pins[pos] = pin;
            Serial.println(pos);
            return;
            }
        }
    for (int i = 0; i<8;i++) {
        if (servo_pins[i] == 0) {pos = i;break;}
        }
    if (pos == -1) {;}
    else {
        servos[pos].attach(pin, min, max);
        servo_pins[pos] = pin;
        Serial.println(pos);
        }
}

void SV_remove(String data) {
    int pos = Str2int(data);
    servos[pos].detach();
    servo_pins[pos] = 0;
}

void SV_read(String data) {
    int pos = Str2int(data);
    int angle;
    angle = servos[pos].read();
    Serial.println(angle);
}

void SV_write(String data) {
    String sdata[2];
    split(sdata,2,data,'%');
    int pos = Str2int(sdata[0]);
    int angle = Str2int(sdata[1]);
    servos[pos].write(angle);
}

void SV_write_ms(String data) {
    String sdata[2];
    split(sdata,2,data,'%');
    int pos = Str2int(sdata[0]);
    int uS = Str2int(sdata[1]);
    servos[pos].writeMicroseconds(uS);
}

void sizeEEPROM() {
    Serial.println(E2END + 1);
}

void EEPROMHandler(int mode, String data) {
    String sdata[2];
    split(sdata, 2, data, '%');
    if (mode == 0) {
        EEPROM.write(Str2int(sdata[0]), Str2int(sdata[1]));
    } else {
        Serial.println(EEPROM.read(Str2int(sdata[0])));
    }
}

// ─────────────────────────────────────────────
//  Serial Parser — LCD komutları eklendi
// ─────────────────────────────────────────────

void SerialParser(void) {
  char readChar[64];
  Serial.readBytesUntil(33,readChar,64);
  String read_ = String(readChar);
  int idx1 = read_.indexOf('%');
  int idx2 = read_.indexOf('$');
  String cmd  = read_.substring(1,idx1);
  String data = read_.substring(idx1+1,idx2);

  if      (cmd == "dw")    { DigitalHandler(1, data); }
  else if (cmd == "dr")    { DigitalHandler(0, data); }
  else if (cmd == "aw")    { AnalogHandler(1, data); }
  else if (cmd == "ar")    { AnalogHandler(0, data); }
  else if (cmd == "pm")    { ConfigurePinHandler(data); }
  else if (cmd == "ps")    { pulseInSHandler(data); }
  else if (cmd == "pi")    { pulseInHandler(data); }
  else if (cmd == "ss")    { SS_set(data); }
  else if (cmd == "sw")    { SS_write(data); }
  else if (cmd == "sr")    { SS_read(data); }
  else if (cmd == "sva")   { SV_add(data); }
  else if (cmd == "svr")   { SV_read(data); }
  else if (cmd == "svw")   { SV_write(data); }
  else if (cmd == "svwm")  { SV_write_ms(data); }
  else if (cmd == "svd")   { SV_remove(data); }
  else if (cmd == "version"){ Version(); }
  else if (cmd == "to")    { Tone(data); }
  else if (cmd == "nto")   { ToneNo(data); }
  else if (cmd == "cap")   { readCapacitivePin(data); }
  else if (cmd == "so")    { shiftOutHandler(data); }
  else if (cmd == "si")    { shiftInHandler(data); }
  else if (cmd == "eewr")  { EEPROMHandler(0, data); }
  else if (cmd == "eer")   { EEPROMHandler(1, data); }
  else if (cmd == "sz")    { sizeEEPROM(); }
  // ── Yeni LCD komutları ──
  else if (cmd == "lci")   { LCD_init(data); }
  else if (cmd == "lcb")   { LCD_backlight(data); }
  else if (cmd == "lcc")   { LCD_clear(data); }
  else if (cmd == "lch")   { LCD_home(data); }
  else if (cmd == "lcs")   { LCD_setCursor(data); }
  else if (cmd == "lcp")   { LCD_print(data); }
  else if (cmd == "lcsp")  { LCD_setCursorPrint(data); }
}

void setup()  {
  Serial.begin(115200);
  while (!Serial) { ; }
  Serial.println("connected");
}

void loop() {
  SerialParser();
}
