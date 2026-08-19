# 8. Zusammenspiel der Softwarekomponenten

Unser Roboter besteht aus mehreren Softwaremodulen, die bereits oben einzeln erklärt wurden. Nun soll darauf eingegangen werden, wie diese Softwarekomponenten in bestimmten Einsatzszenarien miteinander agieren.

## Szenario A: Allgemeine Funktionsweise

Die Software des Roboters besteht aus mehreren Teilen: Zuerst wird die Ausrichtung durch die Spannungswertmessung vom ESP32 angestoßen. Daraufhin erhält das Bildverarbeitungsmodul auf dem Android-Smartphone die Befehlsgewalt über die Steuerungslogik auf dem ESP32, welche wiederum die Antriebssteuerung auf dem Arduino steuert. Diese Module kommunizieren kontinuierlich miteinander, um den Roboter in Richtung der stärksten Lichtquelle zu bewegen. Das Bildverarbeitungsmodul analysiert die Kamerabilder und sendet die erkannten Lichtquellen an den ESP32, der die Steuerdaten an den Arduino weiterleitet. Der Arduino steuert daraufhin die Motoren, um den Roboter entsprechend zu bewegen.

## Userinteraktion: Abdecken der Lichtquelle

In diesem Testszenario deckt ein Benutzer die Lichtquelle mit einem Laken ab. Die Sensoren erkennen die plötzliche Abnahme der Helligkeit, und das Bildverarbeitungsmodul des Smartphones sorgt dafür, dass sich der Roboter nicht mehr bewegt. Diese Information erhält der ESP32 durch das Ablaufen eines 30-sekündigen Stillstand-Timers. Der ESP32 berechnet die neue Richtung basierend auf den empfangenen Solarzellenspannungen und sendet entsprechende Steuerbefehle an den Arduino. Der Roboter justiert sich neu und bewegt sich in Richtung der nächststärkeren Lichtquelle.

## Userinteraktion: Direktes Anleuchten

Bei geringen Lichtverhältnissen kann ein Benutzer den Roboter direkt mit einer Taschenlampe anleuchten. Zuerst erkennt der ESP32 durch die Spannung an den Solarzellen die Richtung. Daraufhin justiert sich der Roboter, und das Bildverarbeitungsmodul erkennt die starke Lichtquelle und leitet die benötigten Steuerungsinformationen an den ESP32 weiter. Der Roboter fährt auf die Lichtquelle zu, was in diesem Fall bedeutet, dass er sich auf den Benutzer zubewegt.

## Standalone-Funktion: Große Fläche

In diesem Szenario wird die Standalone-Funktion des Roboters getestet. Der Roboter wird in einem großen Raum oder auf einem Parkplatz platziert, wo er tagsüber der Sonne folgt und sich nachts an einer künstlichen Lichtquelle, wie einer Straßenlaterne, orientiert. Die Softwaremodule arbeiten zusammen, um die Lichtverhältnisse kontinuierlich zu überwachen. Bei Tag bewegt sich der Roboter autonom in Richtung der Sonnenstrahlen. Bei Nacht erkennt das Bildverarbeitungsmodul das Licht der Laterne, und der Roboter fährt darauf zu. Diese Dunkelheit kann auch in einem Raum simuliert werden, indem die Vorhänge geschlossen werden, wodurch der Roboter zur nächstgelegenen Lichtquelle navigiert. Es ist zu beachten, dass der Roboter noch nicht über eine Kollisionsvermeidung verfügt. Daher sollte dieses Szenario unter Beobachtung eines Menschen durchgeführt werden, und der Raum sollte möglichst groß sein.  

Durch diese verschiedenen Testszenarien wird das Zusammenspiel der Softwaremodule deutlich. Die Bildverarbeitung, die Kommunikation zwischen den Komponenten und die Steuerungslogik arbeiten zusammen, um den Roboter auf Veränderungen in seiner Umgebung reagieren zu lassen und seine Bewegungen entsprechend anzupassen.