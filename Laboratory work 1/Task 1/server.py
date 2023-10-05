import socket
import datetime


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(('localhost', 33333))
serversocket.listen(5)

print('Server waiting for the clients...')

clientsocket, addr = serversocket.accept()
print('Connection from :  {}'.format(addr))
clientsocket.send('Enter your sentence : '.encode('utf-8'))
sentence = clientsocket.recv(1024)
now = datetime.datetime.now()
print(sentence.decode('utf-8') + "\nTime of message : {}".format(now))

clientsocket.close()
