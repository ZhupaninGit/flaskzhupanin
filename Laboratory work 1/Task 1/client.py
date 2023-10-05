import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', 33333))
while True:
    server_responce = s.recv(1024)
    print(server_responce.decode('utf-8'))
    message = input()
    s.send(message.encode('utf-8'))
    server_responce = s.recv(1024)
    print(server_responce.decode('utf-8'))
    if message == "stop":
        print("End of work...")
        break

s.close()
