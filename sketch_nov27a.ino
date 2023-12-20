const int ledPin = 13; // Pin para el LED
const int buzzerPin = 12; // Pin para el buzzer
const int rightButtonPin = 2; // Pin digital para el botón de mover a la derecha
const int leftButtonPin = 4; // Pin digital para el botón de mover a la izquierda

void setup() {
 pinMode(rightButtonPin, INPUT_PULLUP);
 pinMode(leftButtonPin, INPUT_PULLUP);
 pinMode(ledPin, OUTPUT); // Configura el pin del LED como salida
 pinMode(buzzerPin, OUTPUT); // Configura el pin del buzzer como salida
 Serial.begin(9600); // Inicia la comunicación serial a 9600 bps
}

void loop() {
 // Lee el estado de los botones
 int rightButtonState = digitalRead(rightButtonPin);
 int leftButtonState = digitalRead(leftButtonPin);

 // Envia el estado de los botones por el puerto serie
 Serial.print(rightButtonState);
 Serial.print(",");
 Serial.println(leftButtonState);

 // Lee el valor enviado desde Python
 if (Serial.available() > 0) {
  char received = Serial.read();
  if (received == '1') {
    digitalWrite(ledPin, HIGH); // Enciende el LED
    tone(buzzerPin, 100); // Sonido a 1000 Hz
    delay(1000); // Espera 1 segundo
    noTone(buzzerPin); // Detiene el sonido
    digitalWrite(ledPin, LOW);
  }
  if (received == '2'){
    tone(buzzerPin,1000,200);
 }
 }


 delay(100); // Pequeño retardo para evitar saturar el puerto serie
}

