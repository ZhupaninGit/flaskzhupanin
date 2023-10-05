import socket
import time


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serveraddress = ('localhost', 33333)
serversocket.bind(serveraddress)

serversocket.listen(5)

print('Server waiting for the clients...')
clientsocket, addr = serversocket.accept()

print('Connection from :  {}'.format(addr))
clientsocket.send('Enter your sentence : '.encode('utf-8'))
data = clientsocket.recv(1024)
time.sleep(5)
if clientsocket.send(data) == len(data):
    print(f"Sent back: {data.decode()}")
else:
    print("Sent error.")


clientsocket.close()
serversocket.close()
