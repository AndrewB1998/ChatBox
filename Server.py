import socket
import threading    
import subprocess
from cryptography.fernet import Fernet

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 1234

key = Fernet.generate_key()

# Create, bind and accept socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
names = []

def send(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            send(message)
            
            if len(names) > 0:
                send_names = " ".join(names)
                client.send(f"NAMES {send_names}".encode('utf-8'))
            
        except ConnectionResetError:
            idx = clients.index(client)
            clients.remove(client)
            name = names[idx]
            names.remove(name)
            print(f"Client {name} left")
            send(f"User left: {name}".encode('utf-8'))
            break
    
    

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send(f"KEY {key}".encode('utf-8'))
        print(key)
        client.send("NAME".encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        send(f"Welcome to the chat {name}!".encode('utf-8'))
        names.append(name)
        clients.append(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
if __name__ == '__main__':
    # Start the server using subprocess
    subprocess.Popen(["python", "server.py"])

print("Server running...")
receive()