from socket import *


port = 4200

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('192.168.0.72', port))

print('접속 완료')

while True:
    recvData = clientSock.recv(1024) # recv는 메세지 수신 메소드. 1024바이트만큼 데이터를 가지고오겠다.
    print('상대방 :', recvData.decode('utf-8'))

    sendData = input('>>>')
    clientSock.send(sendData.encode('utf-8'))
