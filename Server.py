import socket
import threading    

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 1234


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
            print(message.decode('utf-8'))
            send(message)
            
            if len(names) > 0:
                send_names = " ".join(names)
                client.send(f"NAMES {send_names}".encode('utf-8'))
            
        except:
            idx = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[idx]
            names.remove(name)
            send(f"{name} has left the chat!".encode('utf-8'))
           
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send("NAME".encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        
        names.append(name)
        clients.append(client)
        print(f"Name of the client is {name}")
        send(f"{name} has joined the chat!".encode('utf-8'))
        client.send("Connected to the server!".encode('utf-8'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server running...")
receive()