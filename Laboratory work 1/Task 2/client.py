import threading
import socket

nickName = input("Enter you nickname : \n> ")

socketclient = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketclient.connect(('localhost',33333))

def receiveFromTheChat():
    while True:
        try:
            message = socketclient.recv(1024).decode("utf-8")
            if message == "NICKNAME":
                socketclient.send(nickName.encode("utf-8"))
            else:
                print(message)
        except:
            print("Error!Program finished.")
            socketclient.close()
            break

def writeToTheChat():
    while True:
        newMessage = f'{nickName} : {input("")}'
        socketclient.send(newMessage.encode("utf-8"))

threadToRecieve = threading.Thread(target=receiveFromTheChat)
threadToRecieve.start()

threadToWrite = threading.Thread(target=writeToTheChat)
threadToWrite.start()
