import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', 33333))

server_responce = s.recv(1024)
print(server_responce.decode('utf-8'))

a = input()
s.send(a.encode('utf-8'))

server_responce = s.recv(1024)
print(server_responce.decode('utf-8'))


s.close()
