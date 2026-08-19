# 5. Initiale Entwicklungsplanung
 
Es wird in verschieden Segmente aufgeteilt, welche bestimmte Funktionen erfüllen sollen:  

Benutzerinteraktion: Der Benutzer kann durch Verschattung oder das Schalten von Licht mit dem Roboter interagieren.  

Smartphone: Das Smartphone nutzt die vordere und hintere Kamera zur Lichtsensor-Erkennung. Es analysiert die Lichtverhältnisse und leitet die Richtung zur nächsten Lichtquelle ab.  

Solarzellen: Diese messen kontinuierlich die Spannungswerte und liefern Daten zur Energiegewinnung.  

Python-Programm: Dieses Programm verarbeitet die Bilddaten der Kamera, interpretiert die Lichtpunkte und generiert Steuerungsbefehle für den Roboter, wie den Winkel und die Länge der Motorbewegung.  

Mikrocontroller/Software: Diese Software kontrolliert die Helligkeitsmessungen, speichert die historischen Daten und steuert basierend auf den Messergebnissen die Lenkung und den Antrieb des Roboters.  

Fahrplattform: Der Antrieb des Roboters ermöglicht Drehbewegungen und die Fortbewegung in Richtung der Lichtquelle.  

Die initiale Entwicklungsplanung beschreibt die Struktur und die Funktionsweise des Systems. Die Umsetzung dieser Planung und die detaillierte Implementierung werden in den folgenden Abschnitten beschrieben.  

# 6. Komponentenliste

**Stromversorgung:**  

- Zwei Powerbanks mit 5V für die Mikrocontroller und den Regler
- Eine 12V Powerbank für die Elektromotoren

**Motoren und Antrieb:**  

- Zwei Step Motoren vom Typ 28BYJ-48 12V DC zur Fortbewegung
- Zwei Motortreiber vom Typ A4988 zum einfachen Ansteuern der Motoren
- Ein Tower Pro MG 996R Regler für die Lenkung

**Mikrocontroller und Boards:**  

- Arduino Uno: Steuert die Antriebskomponenten
- CNC Shield: Ermöglicht die einfache Verkabelung von Motoren und Motortreibern
- ESP32: Überträgt die Daten aus dem Netzwerk an den Arduino
- USB-C Adapter: 12V Betriebsspannung auf +/- Anschluss

**Konstruktion:**

- Zwei Plexiglasscheiben als Basis der Grundkonstruktion
- 3D-gedruckte Halterungen und Befestigungen

**Antrieb und Rollen:**

- Ein wiederverwendetes großes Rad für den Antrieb
- Eine feste Rolle für die Lenkung und zwei frei bewegliche Rollen als Stützen

**Gründe für die Auswahl:**

 Viele Komponenten stammten aus dem persönlichen Haushalt und Vorrat der Teammitglieder. Dadurch konnten wir schnell mit der Entwicklung beginnen und mussten nur wenige Teile zukaufen. Lediglich die feste Lenkrolle, die Stützrollen und einige Schrauben zur Montage der Komponenten mussten erworben werden.

