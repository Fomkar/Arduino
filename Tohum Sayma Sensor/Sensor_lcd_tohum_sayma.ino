#include <LiquidCrystal_I2C.h>

#define Button 2
LiquidCrystal_I2C lcd(0x27, 20, 4);

int counter = 0;
long randNumber;
bool buttonPressed = false;

void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);

  pinMode(Button, INPUT_PULLUP);

  generateNewBatch();  // Başlangıçta bir rastgele sayı üret
}

void loop() {
  if (digitalRead(Button) == LOW) {
    if (!buttonPressed) {
      buttonPressed = true;

      counter++;

      // Eksik kalan tohum sayısını azalt
      int remaining = 1000 - randNumber - counter;
      if (remaining < 0) remaining = 0;

      lcd.setCursor(17, 2);
      lcd.print("    ");
      lcd.setCursor(17, 2);
      lcd.print(counter);

      lcd.setCursor(17, 1);
      lcd.print("    ");
      lcd.setCursor(17, 1);
      lcd.print(remaining);

      // Eğer eksik tohum tamamlandıysa yeni rastgele sayı üret
      if (remaining == 0) {
        delay(500);
        generateNewBatch();  // Yeni seri başlat
      }
    }
  } else {
    buttonPressed = false; // Buton bırakıldığında tekrar basılmasına izin ver
  }

  delay(50); // Gereksiz tekrarı önlemek için küçük bir gecikme
}

void generateNewBatch() {
  counter = 0;
  randNumber = random(940, 990);
  Serial.print("Yeni rastgele: ");
  Serial.println(randNumber);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Sayilan Tohum :");
  lcd.setCursor(17, 0);
  lcd.print(randNumber);

  lcd.setCursor(0, 1);
  lcd.print("Eksik Tohum   :");
  lcd.setCursor(17, 1);
  lcd.print(1000 - randNumber);

  lcd.setCursor(0, 2);
  lcd.print("Sensor gelen  :");
  lcd.setCursor(17, 2);
  lcd.print(counter);
}
