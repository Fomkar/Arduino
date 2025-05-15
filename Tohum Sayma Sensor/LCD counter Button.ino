// C++ code
//
#include <LiquidCrystal_I2C.h>

#define Button 2
LiquidCrystal_I2C lcd(0x27, 20, 4);  

int counter = 0;

void setup() {
  lcd.init();
  
  // Arka ışığı açın
  lcd.backlight();
  pinMode(Button, INPUT_PULLUP);
  lcd.setCursor(0, 0);
  lcd.print("counter : 0");
  Serial.begin(9600);
}

void loop() {
  Serial.println("Buttonun Durumu :");
  Serial.println(digitalRead(Button));
  
  if (digitalRead(Button) == LOW) {
    counter++;
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("counter : ");
    lcd.print(counter);
    delay(300); // Butonun titremesini (debounce) önlemek için
  }
}
