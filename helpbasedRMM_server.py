import socket
import threading
import pyautogui
import io
import struct
import time

def send_screenshot(conn):
    while True:
        try:
            # Capture d'écran
            screenshot = pyautogui.screenshot()
            # Enregistrement de l'image dans un tampon mémoire au format JPEG
            buf = io.BytesIO()
            screenshot.save(buf, format='JPEG')
            img_data = buf.getvalue()
            
            # Envoi de la taille de l'image (4 octets en ordre réseau)
            conn.sendall(struct.pack('!I', len(img_data)))
            # Envoi de l'image
            conn.sendall(img_data)
            
            time.sleep(0.5)  # ajustez pour modifier la fréquence des images
        except Exception as e:
            print("Erreur lors de l'envoi du screenshot :", e)
            break

def receive_commands(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode('utf-8').strip()
            print("Commande reçue :", command)
            if command.lower() == "exit":
                break
            # Vous pouvez ajouter ici l'interprétation de commandes (ex. : déplacement de la souris)
            # Exemple (non implémenté) : if command.startswith("move"): ...
        except Exception as e:
            print("Erreur lors de la réception de commande :", e)
            break

def handle_client(conn, addr):
    print("Client connecté :", addr)
    threading.Thread(target=send_screenshot, args=(conn,), daemon=True).start()
    threading.Thread(target=receive_commands, args=(conn,), daemon=True).start()

def main():
    host = '0.0.0.0'  # écoute sur toutes les interfaces réseau
    port = 31337       # port d'écoute (modifiable)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print("Serveur helpbasedRMM en écoute sur {}:{}".format(host, port))
    
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Arrêt du serveur.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
