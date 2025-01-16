# Simple_Botnet
##t.me/VENDOMP

Überblick

Dieses Programm besteht aus zwei Teilen:

    Server-Skript: Läuft kontinuierlich und verbindet sich mit dem Client, sobald dieser aktiv ist.
    Client-Skript: Akzeptiert Verbindungen von mehreren Servern und ermöglicht Interaktionen wie Shell-Befehle, Datei-Upload und Datei-Download. Es bietet auch die Möglichkeit, Befehle an alle Server gleichzeitig zu senden.

Funktionen
Client-Befehle
Befehl	Beschreibung	Beispiel
upload <Dateipfad>	Sendet eine Datei vom Client zum ausgewählten Server.	upload test.txt
download <Dateiname>	Lädt eine Datei vom ausgewählten Server zum Client herunter.	download log.txt
<Shell-Befehl>	Führt beliebige Shell-Befehle auf dem ausgewählten Server aus.	dir, ls, echo
all	Aktiviert den Multi-Befehl-Modus, um einen Befehl an alle verbundenen Server gleichzeitig zu senden.	all → dir
exit / quit	Trennt die Verbindung zum aktuellen Server.	exit
Server-Funktionen

    Dauerhafte Verbindung: Der Server versucht kontinuierlich, sich mit dem Client zu verbinden, bis die Verbindung erfolgreich ist.
    Shell-Zugriff: Führt Befehle aus, die der Client sendet.
    Dateioperationen:
        Upload: Speichert Dateien, die der Client sendet.
        Download: Sendet angeforderte Dateien an den Client.

Anleitung zur Nutzung
1. Server-Skript starten

    Starte das Server-Skript auf den Maschinen, die überwacht werden sollen.
    Das Skript läuft kontinuierlich und versucht, sich mit dem Client zu verbinden.

2. Client-Skript starten

    Starte das Client-Skript auf deiner lokalen Maschine.
    Das Skript wartet auf eingehende Verbindungen von den Servern.

3. Verbindung verwalten

    Sobald Server verbunden sind, werden sie in einer Liste angezeigt.
    Wähle den Server durch Eingabe von Befehlen aus, um mit ihm zu interagieren.

4. Multi-Befehl-Modus

    Gib all ein, um Befehle gleichzeitig an alle Server zu senden.

Beispiele
1. Datei hochladen

192.168.1.10 > upload test.txt
Datei test.txt erfolgreich hochgeladen.

2. Datei herunterladen

192.168.1.10 > download log.txt
Datei log.txt erfolgreich heruntergeladen.

3. Shell-Befehl ausführen

192.168.1.10 > dir
 Ausgabe:
 Datei1.txt
 Datei2.log

4. Multi-Befehl-Modus

all
Befehl für alle Server > dir
[192.168.1.10] Ausgabe:
 Datei1.txt
 Datei2.log

[192.168.1.11] Ausgabe:
 Datei3.txt
 Datei4.log

Technische Hinweise

    Port und IP-Adressen:
        Standardmäßig läuft der Client auf Port 12345.
        Stelle sicher, dass der Port nicht durch eine Firewall blockiert wird.
    Dateien:
        Hochgeladene Dateien werden im aktuellen Arbeitsverzeichnis des Servers gespeichert.
        Heruntergeladene Dateien werden mit dem Präfix downloaded_ im Client-Verzeichnis gespeichert.
    Fehlerbehandlung:
        Der Client versucht, Verbindungsabbrüche zu erkennen und die Verbindung wiederherzustellen.
        Stelle sicher, dass die Netzwerkverbindung stabil ist.

Autostart einrichten (Windows)
Für den Server

    Erstelle eine .bat-Datei:

    python pfad_zum_server_skript.py

    Füge die .bat-Datei in den Windows-Startup-Ordner ein:
        Drücke Win + R → Gib shell:startup ein → Kopiere die .bat-Datei in den Ordner.

Empfohlene Erweiterungen

    Sicherheit:
        Füge ein Passwort oder eine Authentifizierung hinzu, um unbefugte Zugriffe zu verhindern.
        Nutze SSL-Verschlüsselung (ssl-Modul) für sichere Kommunikation.
    Logging:
        Protokolliere alle Befehle und Dateibewegungen für Transparenz.
    Mehr Funktionen:
        Ergänze weitere Shell-Befehle oder Dateioperationen nach Bedarf.

Viel Erfolg beim Einsatz des Tools!
