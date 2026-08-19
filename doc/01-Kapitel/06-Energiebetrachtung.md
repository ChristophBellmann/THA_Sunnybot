# 9. Energiebetrachtung

: Systemleistungsaufnahme  

| Komponente | Leistungsaufnahme
|----------------|-------------------|
|Motor:	|	6 W (typ., begrenzt durch Motorsteuerung)|
|Servo Lenkung:|	5.5 W (typ.) / 15 W (peak)|
|Motorsteuerung: |	1 W (geschätzt)|
|Arduino Uno: |	0,40 W (typ. Verbrauch)|
|ESP32:	|	0,63 W (typ. Verbrauch WLAN Betrieb)|

Gesamtsystemleistung: 13,53 W  

Es sind 3 Powerbanks eingesetzt:

- Versorgung Motoren + Motorsteuerung (12 V, 20000 mAh; 19,2 h Betrieb)
- Versorgung Arduino (5 V, 5000 mAh; 62 h Betrieb)
- Versorgung ESP 23 (5 V, 10000 mAh; 80 h Betrieb)

Es wurden mittlere Verbräuche angegeben, je nach Betriebszustand können diese höher oder niedriger ausfallen, auch wurden Verluste der Powerbanks nicht berücksichtigt. Das Smartphone zur Steuerung und Bilderkennung wird autark betrieben, hier sind keine langfristigen Verbrauchswerte bekannt. Es ist allerdings davon auszugehen, dass die Laufzeit des Systems durch die des Smartphones beschränkt wird.  

Theoretisch wäre ein Betrieb ohne Smartphone möglich bei dem nur die Solarzellen als Sensoren verwendet werden, hier wäre eine Betrieb von ca. 19 Stunden möglich, wenn die Motte permanent fährt.  