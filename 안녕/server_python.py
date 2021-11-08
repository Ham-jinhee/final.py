# from socket import *
# import threading #스레딩과 타임을 추가해줍니다.
# import time
#
# def send(data):
#     while True:
#         SendData=input('>')
#         data.send(SendData.encode('utf-8'))
#
# def receive(data):
#     while True:
#         recvData=data.recv(1024)
#         print('메세지: ',recvData.decode('utf-8'))
#
# port=4200
#
# svrsock=socket(AF_INET,SOCK_STREAM)
# svrsock.bind(('localhost',port)) #변수를 port로 만들어줍니다.
# svrsock.listen(1)
#
# conn,addr=svrsock.accept() #accept로 받아줍니다.
#
# sender=threading.Thread(target=send,args=(conn,)) #튜플이니까 , 를 찍어줍니다.
# #target으로 send 받아주고 args로 conn, 을 받아줄 겁니다.
# receiver=threading.Thread(target=receive,args=(conn,))
#
# sender.start()
# receiver.start()
#
# while True:
#     time.sleep(1)
#     pass
# #스레드를 만들어 줬으니 실행을 해야합니다.
# print("서버 접속 완료")

######################################################################################

# #코드
# from socket import *
# import threading #스레딩과 타임을 추가해줍니다.
# import time
#
# def send(data):
#     while True:
#         msg = data.input_message.text()
#         data.send(msg.encode('utf-8'))
#
# def receive(data):
#     while True:
#         recvData=data.recv(1024)
#         print('메세지: ',recvData.decode('utf-8'))
#
# port=4200
#
# svrsock=socket(AF_INET,SOCK_STREAM)
# svrsock.bind(('localhost',port)) #변수를 port로 만들어줍니다.
# svrsock.listen(1)
#
# conn,addr=svrsock.accept() #accept로 받아줍니다.
#
# sender=threading.Thread(target=send,args=(conn,)) #튜플이니까 , 를 찍어줍니다.
# #target으로 send 받아주고 args로 conn, 을 받아줄 겁니다.
# receiver=threading.Thread(target=receive,args=(conn,))
#
# sender.start()
# receiver.start()
#
# while True:
#     time.sleep(1)
#     pass
# #스레드를 만들어 줬으니 실행을 해야합니다.

from socket import *

port = 5200

serverSock = socket(AF_INET, SOCK_STREAM) # 소켓 생성
serverSock.bind(('', port)) # 생성한 소켓 bind - 클라이언트 만들때는 불필요, 서버를 운용할때는 반드시 필요.
                            # 생성된 소켓의 번호와 실제 어드레스 패밀리를 연결해주는 것
serverSock.listen(5) # 접속을 기다리는 단계로 넘어감, ()안의 숫자는 몇개까지 동시접속을 허용할 것 인가.

print('%d번 포트로 접속 대기중...'%port)

connectionSock, addr = serverSock.accept() # 접속을 허락하고, 통신을 하기 위해.
# 서버에 접속한 상대방과 데이터를 주고받기 위해서 accept를 통해 생성된 connectionSock을 사용하면됨.
# 이제부터 serverSock보다는 connectionSock을 이용.
print(str(addr), '에서 접속되었습니다.')

while True:
    print("메세지 받기")
    msg = input('>>>')
    connectionSock.send(msg.encode('utf-8'))

    recvData = connectionSock.recv(1024)
    print('상대방 :', recvData.decode('utf-8'))


