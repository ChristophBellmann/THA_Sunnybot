// Set power output on A4988 Stepper Motor controller
// U = 12 V, I should be limited to around 0.5 A for a power output of max. 6 Watt
// The current can be limited via a potentiometer on the motor controller board.
// The potentiometer sets a reference voltage which is proportional to the current limit .
// current limit = VRef * 2.5
// Vref set to 0.2 V equals a max. current of 0.5 A.
// That way the motor power is limited to 6 W.


//Includes
#include <SoftwareSerial.h> //Wird verwendet um die Seriellen Schnittstellen innerhalb der Software zu unterscheiden 
#include <Servo.h> //Lib für Servo-Ansteurung

// Definiere die Pins für SoftwareSerial
SoftwareSerial mySerial(0, 1); // RX, TX
// Servo-Objekt erstellen
Servo myServo;

bool dirFlag = false;

//Variables
float vel = 0; //Geschwindigkeit in Meter pro Sekunde
const float maxVel = 0.175; //Maximale Geschwindigkeit 
int ang = 0; //Servo Winkel
float motorSpeed = 0; // Geschwindigkeit der Schrittmotoren in Mikrosekunden

// Definiere die Pins für die Motoren
const int stepPinX = 2;
const int dirPinX = 5;
const int stepPinY = 3;
const int dirPinY = 6;
const int enablePin = 8;


//Setup - Initialisierung 
void setup(){
Serial.begin(9600); // Serieller Monitor - Nachrichten werden als Ausgabe beschrieben 
mySerial.begin(9600); // SoftwareSerial für Kommunikation mit ESP32
Serial.println("Arduino bereit"); //Ausgabe: Start Arduino
myServo.attach(9); // Servo-Pin definieren (es wird der X Limit + Pin verwendet, welchen wir für die Motortreiber nicht benötigen)
// Motor-Pins als Ausgang definieren
pinMode(stepPinX, OUTPUT);
pinMode(dirPinX, OUTPUT);
pinMode(stepPinY, OUTPUT);
pinMode(dirPinY, OUTPUT);
pinMode(enablePin, OUTPUT);
// enables A4988 stepper drivers, pin 8, 0 = enable, 1 = disable
digitalWrite(8, 0);
}

void parseMessage(String message) {
  int vIndex = message.indexOf("V=");
  int alphaIndex = message.indexOf(" Alpha=");
  if (vIndex != -1 && alphaIndex != -1) {
    String velStr = message.substring(vIndex + 2, alphaIndex);
    String angStr = message.substring(alphaIndex + 7);

    vel = velStr.toFloat();
    ang = angStr.toInt();
  } else {
    Serial.println("Ungültiges Nachrichtenformat");
  }
}

//Loop - Dauerhafte Wiederholung 
void loop(){
//Aktualisieren, falls Daten vom ESP32 kommen und schreiben in Variable vom Arduino
if (mySerial.available()) {
  String message = mySerial.readStringUntil('\n'); // Einlesen der empfangenen Nachricht in Variable
  Serial.print("Empfangene Nachricht: ");
  Serial.println(message); // Ausgabe: Empfangene Nachricht vom ESP32

  // Verarbeiten der Nachricht und Aktualisieren der Variablen
  parseMessage(message);
  Serial.print("Aktualisierte Werte - vel: "); // Ausgabe:
  Serial.print(vel); // Ausgabe: Wert vel
  Serial.print(", ang: "); // Ausgabe:
  Serial.println(ang); // Ausgabe Wert: ang

  // Begrenze die Geschwindigkeit auf die maximale erlaubte Geschwindigkeit
  if (vel > maxVel) {
    vel = maxVel;
  }
  myServo.write(ang); //Ansteuerung des Reglers mit Hilfe der Variable ang: Setzt immer auf den Aktuellsten Wert

  // Geschwindigkeit basierend auf vel in Schritte pro Mikrosekunde umrechnen
  float umdrehungenProSekunde = vel / 0.471; //Umdrehungen pro Sekunde basierend auf Geschwindigkeit in m/s: rps = vel / 0.471(Radumfang in Metern, berechnet als 2*π*0.075m)
  float schritteProSekunde = umdrehungenProSekunde * 2048; //// Berechne die Anzahl der Schritte pro Sekunde: eine Umdrehung = 2048 Schritte
  motorSpeed = 1e6 / schritteProSekunde; // Mikrosekunden pro Schritt 1e6 = 1 Mikrosekunde
}

// set the direction once to forward.
if (dirFlag == false) { //run once
  // Set direction for X and Y axes
  digitalWrite(5, 0); // Set X direction
  digitalWrite(6, 1); // Set Y direction
  dirFlag = true;
}

//motorSpeed = 1e6 / 0.5 * 2048;

// Motorensteuerung basierend auf motorSpeed
if (motorSpeed > 0) {
    digitalWrite(stepPinX, HIGH);
    delayMicroseconds(10); // Short pulse for step signal
    digitalWrite(stepPinX, LOW);

    digitalWrite(stepPinY, HIGH);
    delayMicroseconds(10); // Short pulse for step signal
    digitalWrite(stepPinY, LOW);
    delayMicroseconds(motorSpeed);
  }
}