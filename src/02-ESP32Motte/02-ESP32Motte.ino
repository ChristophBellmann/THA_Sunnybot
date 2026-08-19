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
float velocity = 0.0;
int alpha = 0;
bool debugMode = false;

//Pinout Solarzellen: Front, Back, Left, Right, Top
const int PinF = 32, PinB = 34, PinL = 35, PinR = 39, PinT = 33;

//Values Solarzellen: Front, Back, Left, Right, Top
int ValF = 0, ValB = 0, ValL = 0, ValR = 0, ValT = 0;

// History for calculating mean Values of Luminescence
const int historydepth = 3;
int historyF[historydepth] = {0}, historyB[historydepth] = {0};
int historyL[historydepth] = {0}, historyR[historydepth] = {0};
int historyT[historydepth] = {0};

int meanValF = 0, meanValB = 0, meanValL = 0, meanValR = 0, meanValT = 0;

bool brightness_dropped = false;
bool Androidcontrol = false;
unsigned long lastUpdate = 0;
unsigned long androidControlStartTime = 0;
const unsigned long updateInterval = 1000; // 1 second
const unsigned long androidControlTimeout = 30000; // 30 seconds
const float happyness_threshold = 0.5; // 50 % difference between actual value and mean value

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
  if (millis() - lastUpdate >= updateInterval) {
    lastUpdate = millis();
    saveSensorValues();
    calculateMeanValues();
    checkBrightness();
  }
  
  if (brightness_dropped && !Androidcontrol) {
    performRotation();
  }

  if (Androidcontrol && (millis() - androidControlStartTime >= androidControlTimeout)) {
    Androidcontrol = false;
    logMessage("Android control reset after timeout.");
  }

  parsePacket();

  delay(100); // Kurze Verzögerung, um die serielle Kommunikation nicht zu überlasten
}

void parsePacket() {
  int packetSize = udp.parsePacket(); // Suche nach einkommendem Paket
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0;
    }
    // Check for debug mode commands
    if (strcmp(incomingPacket, "debug") == 0) {
      debugMode = true;
      logMessage("Debug mode enabled.");
    } else if (strcmp(incomingPacket, "nodebug") == 0) {
      debugMode = false;
      logMessage("Debug mode disabled.");
    } else {
      // Only when the Luminescence changed and the Rotation is not in progress.
      if (brightness_dropped || Androidcontrol) { // move the robot remotely 
        logMessage(String("Eingehendes Paket: ") + incomingPacket);
        sscanf(incomingPacket, "V=%f Alpha=%d", &velocity, &alpha); // Bitte in dieser Form die Anfrage vom Handy senden: V=Wert Alpha=Wert

        if (velocity > 0.175) velocity = 0.175;

        logMessage(String("Velocity gesetzt auf: ") + String(velocity, 2) + ", Alpha gesetzt auf: " + String(alpha));
        MySerial.printf("V=%.3f Alpha=%d\n", velocity, alpha);

        udp.beginPacket(udp.remoteIP(), udp.remotePort());
        udp.printf("%.2f , %d", velocity, alpha);
        udp.endPacket();
      } else {
        udp.beginPacket(udp.remoteIP(), udp.remotePort());
        udp.printf("No brightness change or performing Rotation");
        udp.endPacket();
      }
    }
  }
}

void saveSensorValues() {
  for (int i = historydepth - 1; i > 0; i--) {
    historyF[i] = historyF[i - 1];
    historyB[i] = historyB[i - 1];
    historyL[i] = historyL[i - 1];
    historyR[i] = historyR[i - 1];
    historyT[i] = historyT[i - 1];
  }
  
  historyF[0] = analogRead(PinF);
  historyB[0] = analogRead(PinB);
  historyL[0] = analogRead(PinL);
  historyR[0] = analogRead(PinR);
  historyT[0] = analogRead(PinT);
}

void calculateMeanValues() {
  // reset Values to 0
  meanValF = 0, meanValB = 0, meanValL = 0, meanValR = 0, meanValT = 0;

  for (int i = 0; i < historydepth; i++) {
    meanValF += historyF[i];
    meanValB += historyB[i];
    meanValL += historyL[i];
    meanValR += historyR[i];
    meanValT += historyT[i];
  }

  meanValF /= historydepth;
  meanValB /= historydepth;
  meanValL /= historydepth;
  meanValR /= historydepth;
  meanValT /= historydepth;
}

void checkBrightness() {
  if (historyF[0] < meanValF * happyness_threshold ||
      historyB[0] < meanValB * happyness_threshold ||
      historyL[0] < meanValL * happyness_threshold ||
      historyR[0] < meanValR * happyness_threshold ||
      historyT[0] < meanValT * happyness_threshold) {
    brightness_dropped = true;
  } else {
    brightness_dropped = false;
  }
}

void performRotation() {
  int maxValF = 0, maxValB = 0, maxValL = 0, maxValR = 0, maxValT = 0;
  int maxStepF = 0, maxStepB = 0, maxStepL = 0, maxStepR = 0, maxStepT = 0;

  for (int i = 1; i <= 10; i++) {
    MySerial.printf("V=0.175 Alpha=35\n"); // Starten der Drehbewegung. Hm, das wird ein echt großer Kreis, hoffe der Platz reicht aus.
    delay(1640);  // 1.64 Sekunden = Zeit die für eine Umdrehung von 36 Grad benötigt wird
    MySerial.printf("V=0 Alpha=0\n"); // Stoppen der Drehbewegung für erneute Prüfung

    // Read sensor values for each rotation step
    int avgValF360 = analogRead(PinF);
    int avgValB360 = analogRead(PinB);
    int avgValL360 = analogRead(PinL);
    int avgValR360 = analogRead(PinR);
    int avgValT360 = analogRead(PinT);

    // Update max values and steps
    if (avgValF360 > maxValF) {
      maxValF = avgValF360;
      maxStepF = i;
    }
    if (avgValB360 > maxValB) {
      maxValB = avgValB360;
      maxStepB = i;
    }
    if (avgValL360 > maxValL) {
      maxValL = avgValL360;
      maxStepL = i;
    }
    if (avgValR360 > maxValR) {
      maxValR = avgValR360;
      maxStepR = i;
    }
    if (avgValT360 > maxValT) {
      maxValT = avgValT360;
      maxStepT = i;
    }
    // Print intermediate information about the Luminescence at each Rotation step, commented out:
    // logMessage(String("Rotation Angle ") + String(i * 36) + " - LumFront: " + String(avgValF360) + ", LumBack: " + String(avgValB360) + ", LumLeft: " + String(avgValL360) + ", LumRight: " + String(avgValR360) + ", LumTop: " + String(avgValT360));
  }
  
  logMessage(String("Max Values - MaxLumFront: ") + maxValF + " at Angle " + (maxStepF * 36) + ", MaxLumBack: " + maxValB + " at Angle " + (maxStepB * 36) + ", MaxLumLeft: " + maxValL + " at Angle " + (maxStepL * 36) + ", MaxLumRight: " + maxValR + " at Angle " + (maxStepR * 36) + ", MaxLumTop: " + maxValT + " at Angle " + (maxStepT * 36));

  // Find the overall maximum value and its corresponding step
  int maxLum = max(maxValF, max(maxValB, max(maxValL, max(maxValR, maxValT))));
  int maxLumAngle;
  if (maxLum == maxValF) {
    maxLumAngle = maxStepF * 36;
  } else if (maxLum == maxValB) {
    maxLumAngle = maxStepB * 36;
  } else if (maxLum == maxValL) {
    maxLumAngle = maxStepL * 36;
  } else if (maxLum == maxValR) {
    maxLumAngle = maxStepR * 36;
  } else {
    maxLumAngle = maxStepT * 36;
  }
  // To include the Top might be trouble, but could work well also because at that Angle the Luminescence is highest.
  logMessage(String("Highest Brightness: ") + maxLum + " at Angle " + maxLumAngle);

  // to align the robot to this new Angle, drive forward a bit
  MySerial.printf("V=0.17 Alpha=%d\n", maxLumAngle);
  delay(1000);
  MySerial.printf("V=0.0 Alpha=0\n");

  // reset
  brightness_dropped = false;
  Androidcontrol = true;
  androidControlStartTime = millis(); // androidControlTimeout set to 30 s
}

// Log message to Serial and optionally to UDP if debug mode is enabled
void logMessage(String message) {
  Serial.println(message);
  if (debugMode) {
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.print(message);
    udp.endPacket();
  }
}
