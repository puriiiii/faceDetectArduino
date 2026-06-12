const int ledPin = 9;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600); // Must match the baud rate in the Python script
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == '1') {
      digitalWrite(ledPin, HIGH); 
    } else if (command == '0') {
      digitalWrite(ledPin, LOW);  
    }
  }
}
