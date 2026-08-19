// Test Platform: using arduino IDE 2.3.2 with ESP32 Wrover Module

#include <WiFi.h>
#include <WiFiUdp.h>
#include <HardwareSerial.h>

// Netzwerk
const char *ssid = "Sunnybot-Motte-ESP32";
const char *password = "sunnybotmotte";
IPAddress local_IP(192,168,10,100);
IPAddress gateway(192,168,10,100);
IPAddress subnet(255,255,255,0);
WiFiUDP udp;
unsigned int localUdpPort = 4210;  // Der Port, an dem der ESP32 auf Nachrichten wartet
char incomingPacket[255];

// Variablen
int velocity = 0;
int alpha = 0;

int count = 0;

HardwareSerial MySerial(1); // Initialisierung des HardwareSerial1

void setup() {
  MySerial.begin(9600, SERIAL_8N1, 16, 17); // RX, TX Pins für den HardwareSerial1 (ESP32)
  Serial.begin(115200); // Serieller Monitor 

  // Starten des Access Points mit fester IP-Adresse
  if (!WiFi.softAPConfig(local_IP, gateway, subnet)) {
    Serial.println("AP-Konfiguration fehlgeschlagen");
  }
  if (!WiFi.softAP(ssid, password)) {
    Serial.println("AP-Initialisierung fehlgeschlagen");
  }

  Serial.println("Access Point gestartet");
  Serial.print("IP Adresse: ");
  Serial.println(WiFi.softAPIP());

  udp.begin(localUdpPort);
  Serial.print("UDP server gestartet, auf Port: ");
  Serial.println(localUdpPort);
}

void loop() {
  int packetSize = udp.parsePacket(); // Suche nach einkommendem Paket
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0;
    }
    Serial.printf("Eingehendes Paket: %s\n", incomingPacket);

    // Verarbeiten der Nachricht
    sscanf(incomingPacket, "V=%d Alpha=%d", &velocity, &alpha); // Bitte in dieser Form die Anfrage vom Handy senden: V=Wert Alpha=Wert
    Serial.printf("Velocity gesetzt auf: %d, Alpha gesetzt auf: %d\n", velocity, alpha);

    // Senden der Werte als Paket über die serielle Schnittstelle
    MySerial.printf("V=%d Alpha=%d\n", velocity, alpha);

    // Antwort an den Absender
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.printf("%d , %d", velocity, alpha);
    udp.endPacket();
  }

  delay(100); // Kurze Verzögerung, um die serielle Kommunikation nicht zu überlasten

  debug
  count ++;
  Serial.println(count);
  Serial.println("hello world");
}
