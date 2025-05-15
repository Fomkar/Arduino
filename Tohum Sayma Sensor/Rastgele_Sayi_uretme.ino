long randNumber;
void setup() {
  Serial.begin(9600);

}

void loop() {
  // print a random number from 0 to 299
  // print a random number from 10 to 19
  randNumber = random(940, 990);
  Serial.println(randNumber);

  delay(5000);
}
