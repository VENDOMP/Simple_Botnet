import socket
import threading

connections = []

def handle_server(server_socket, address):
    """
    Handhabt die Kommunikation mit einem einzelnen Server.
    """
    print(f"Neue Verbindung von {address}")
    while True:
        try:
            command = input(f"{address} > ")
            if command.lower() in ["exit", "quit"]:
                break

            if command.startswith("upload"):
                _, filepath = command.split(maxsplit=1)
                upload_file(server_socket, filepath)

            elif command.startswith("download"):
                _, filename = command.split(maxsplit=1)
                download_file(server_socket, filename)

            elif command.lower() == "all":
                # Aktiviert den Multi-Befehl-Modus
                broadcast_to_all()

            else:
                execute_command(server_socket, command)

        except (ConnectionResetError, BrokenPipeError):
            print(f"Verbindung zu {address} unterbrochen.")
            break
    server_socket.close()

def upload_file(server_socket, filepath):
    """
    Läd eine Datei vom Client zum Server hoch.
    """
    try:
        filename = filepath.split("/")[-1]
        server_socket.send(f"UPLOAD {filename}".encode())
        with open(filepath, "rb") as f:
            while chunk := f.read(1024):
                server_socket.send(chunk)
        print(f"Datei {filename} erfolgreich hochgeladen.")
    except FileNotFoundError:
        print("Fehler: Datei nicht gefunden.")
    except Exception as e:
        print(f"Fehler beim Hochladen: {e}")

def download_file(server_socket, filename):
    """
    Läd eine Datei vom Server herunter.
    """
    try:
        server_socket.send(f"DOWNLOAD {filename}".encode())
        with open(f"downloaded_{filename}", "wb") as f:
            while True:
                data = server_socket.recv(1024)
                if data.endswith(b"<EOF>"):  # Ende der Datei erreicht
                    f.write(data[:-5])
                    break
                f.write(data)
        print(f"Datei {filename} erfolgreich heruntergeladen.")
    except Exception as e:
        print(f"Fehler beim Herunterladen: {e}")

def execute_command(server_socket, command):
    """
    Führt einen Shell-Befehl auf einem Server aus.
    """
    server_socket.send(command.encode())
    response = server_socket.recv(4096).decode()
    print(f"Ausgabe:\n{response}")

def broadcast_to_all():
    """
    Sendet einen Befehl an alle verbundenen Server.
    """
    command = input("Befehl für alle Server > ")
    threads = []
    for conn, addr in connections:
        thread = threading.Thread(target=execute_command_for_all, args=(conn, addr, command))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def execute_command_for_all(conn, addr, command):
    """
    Führt einen Shell-Befehl auf einem Server aus und zeigt die Ergebnisse an.
    """
    try:
        conn.send(command.encode())
        response = conn.recv(4096).decode()
        print(f"[{addr}] Ausgabe:\n{response}")
    except Exception as e:
        print(f"Fehler bei {addr}: {e}")

def start_client():
    """
    Startet den Client, um Verbindungen von Servern entgegenzunehmen.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)
    print("Client läuft und wartet auf Verbindungen...")

    while True:
        client_socket, client_address = server_socket.accept()
        connections.append((client_socket, client_address))
        thread = threading.Thread(target=handle_server, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_client()
