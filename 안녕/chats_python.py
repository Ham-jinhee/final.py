# from socket import *
# import threading
# import time
#
# def send(data):
#     while True:
#         sendData=input('>')
#         data.send(sendData.encode('utf-8')) #인자값으로 클라이언트 소켓을 받아야 합니다. 소켓 데이터값.
#
# def receive(data):
#     while True:
#         recvData=data.recv(1024)
#         print('상대방: ',recvData.decode('utf-8'))
#
# port=4200
#
# clientsock=socket(AF_INET,SOCK_STREAM)
# clientsock.connect(('localhost',port))
#
# sender=threading.Thread(target=send,args=(clientsock,))
# receiver=threading.Thread(target=receive, args=(clientsock,))
#
# sender.start()
# receiver.start()
#
# while True:
#     time.sleep(1)
#     pass
#
#

#코드
from socket import *
import threading
import time

def send(data):
    while True:
        sendData=input('>')
        data.send(sendData.encode('utf-8')) #인자값으로 클라이언트 소켓을 받아야 합니다. 소켓 데이터값.

def receive(data):
    while True:
        recvData=data.recv(1024)
        print('상대방: ',recvData.decode('utf-8'))

port=8050

clientsock=socket(AF_INET,SOCK_STREAM)
clientsock.connect(('localhost',port))

sender=threading.Thread(target=send,args=(clientsock,))
receiver=threading.Thread(target=receive, args=(clientsock,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass