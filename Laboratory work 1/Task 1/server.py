import socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serveraddress = ('localhost', 33333)
serversocket.bind(serveraddress)

serversocket.listen(5)

print('Server waiting for the clients...')
clientsocket, addr = serversocket.accept()

print('Connection from :  {}'.format(addr))
data = ""
clientsocket.send('Enter your sentence (enter `stop` if you want stop conservation): '.encode('utf-8'))
data = clientsocket.recv(1024)
while True:
    sent = clientsocket.send(data)
    if sent == len(data):
        print(f"Sent back: {data.decode()}")
    else:
        print("Sent Error!")
    clientsocket.send('Enter your sentence (enter `stop` if you want stop conservation): '.encode('utf-8'))
    data = clientsocket.recv(1024)
    if data.decode() == "stop":
        break

print("End of work...")
clientsocket.close()
serversocket.close()

