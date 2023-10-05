import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', 33333))
serverresponce = s.recv(1024)
print(serverresponce.decode('utf-8'))
a = input()
s.send(a.encode('utf-8'))
serverresponce = s.recv(1024)
print(serverresponce.decode('utf-8'))

