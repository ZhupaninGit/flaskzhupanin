import threading
import socket

socketserver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketserver.bind(('localhost',33333))
socketserver.listen()

clients = []
nickNames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            messageToSent = client.recv(1024)
            broadcast(messageToSent)
        except:
            indexOfClient = clients.index(client)
            del clients[indexOfClient]
            client.close()
            broadcast("User {} left the chat!".format(nickNames[indexOfClient]).encode("utf-8"))
            del nickNames[indexOfClient]
            break

def connectClient():
    while True:
        client,adrress = socketserver.accept()
        print('Connection from :  {}'.format(adrress))
        client.send("NICKNAME".encode("utf-8"))
        nickName = client.recv(1024).decode("utf-8")
        nickNames.append(nickName)
        clients.append(client)

        broadcast("{} joined the chat!".format(nickName).encode("utf-8"))
        client.send("Successfully conected to the chat,{}!".format(nickName).encode("utf-8"))
        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

print('Server waiting for the clients....')
connectClient()

