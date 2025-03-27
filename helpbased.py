import socket
import struct
import cv2
import numpy as np

def receive_screenshots(client_socket):
    data = b""
    payload_size = struct.calcsize('!I')
    while True:
        try:
            # Récupération de la taille de l'image
            while len(data) < payload_size:
                packet = client_socket.recv(4096)
                if not packet:
                    return
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack('!I', packed_msg_size)[0]
            
            # Récupération des données de l'image
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            img_data = data[:msg_size]
            data = data[msg_size:]
            
            # Conversion des octets en tableau numpy et décodage de l'image
            np_data = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            
            # Affichage de l'image
            cv2.imshow('Remote Desktop - helpbasedRMM', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print("Erreur lors de la réception de screenshot :", e)
            break

    client_socket.close()
    cv2.destroyAllWindows()

def main():
    host = input("Entrez l'adresse IP du serveur : ")
    port = 31773 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connecté au serveur helpbasedRMM sur {}:{}".format(host, port))
    
    receive_screenshots(client_socket)

if __name__ == "__main__":
    main()
