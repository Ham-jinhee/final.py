import socket
import threading
import time
import pymysql
import pandas as pd

Host = '10.10.21.118'
PORT = 9500

conn = pymysql.connect(host='10.10.21.118', port=3306, user='root', password='starDB1234@', db='starDB',
                       charset='utf8')
cur = conn.cursor()  #DB연결

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(server)#소켓생성
server.bind((Host, PORT)) #서버 열기
server.listen() #접속가능인원 대기

clients = [] #접속유저 리스트-클라이언트 구분용
nicknames = [] #접속유저 닉네임리스트 -UI 유저리스트용
room_dic = {'temp_room': []} #temp_room=대기창 // key:채팅방 value: 참여유저
room_pw = {'temp_room': []} #비밀채팅방용 //key:비밀채팅방 value:비밀번호
user_id = '' #회원가입 & 로그인 확인용 - 유저아이디
user_pw = '' #회원가입 & 로그인 확인용 - 유저비밀번호

#1 신호 받기(서버연결동안 계속 실행중)
def receive():
    while True:
        client, address = server.accept()
        clients.append(client)
        print("c:",client)
        print("a:",address)
        print("s:",server)

        chat_thread = threading.Thread(target=handle, args=(client,))
        chat_thread.start()

#2 신호메세지 구분하기
def handle(client):
    while True:
        try:
            print('wait...')
            message = client.recv(1024).decode() #클라이언트가 보낸 신호메세지 받기
            print(message)
            if not message: #클라이언트 응답 없을시
                log_out(client) #로그아웃
                break

            elif '#signup' in message: #회원가입
                signup(message, client)

            elif '#my_id_pw' in message: #로그인
                user_login(message, client)
                continue

            elif '#onlineusers' in message: #온라인유저와 채팅방목록 전송
                send_onlineuser_and_chattingroom()

            elif '#refresh' in message: # 온라인유저와 채팅방목록 전송
                send_onlineuser_and_chattingroom()

            elif '#makeroom' in message: #방만들기
                make_room(message)

            elif '#roomjoin' in message: #채팅방 입장(더블클릭)
                join_room(message)
                continue

            elif '#okay' in message: #채팅방 입장(더블클릭)
                join_room(message)

            elif '#exit' in message: #채팅방 나가기
                exit_room(message)

            elif '#invite' in message: #방 초대하기
                invite_room(message)

            elif '#makepwroom' in message: #비밀채팅방 만들기
                make_pw_room(message)

            elif '#pwroomjoin' in message: #비밀채팅방 입장
                join_pw_room(message)

            elif '#idcheck' in message: #아이디 중복체크
                id_check(message, client)

            else:
                chatting(message)  #채팅

        except: #클라이언트 신호 오류시 로그아웃처리
            log_out(client)
            print('after exit : ', clients, nicknames, room_dic)
            break
#3 로그아웃함수
def log_out(client):
    index = clients.index(client)
    nickname = nicknames[index]
    print(nickname, ' out')
    nicknames.remove(nickname)  #접속중인 유저 닉네임 리스트에서 제외하기
    for i in room_dic.keys():
        if nickname in room_dic[i]:
            room_dic[i].remove(nickname)  #채팅방에서 유저 제외하기
            if room_dic[i] != 'temp_room': #로그아웃한 유저가 어떤 채팅방에 있었는지 확인
                room_name = room_dic[i]
                print('after logout' , room_name)
    if len(room_name) < 1: #그 채팅방에 참여한 유저가 아무도 없으면 방 삭제
        del room_name
    clients.remove(client) #접속중인 클라이언트 리스트에서 최종 제외
    print(clients)
    client.close() #클라이언트 연결 종료



#4 DB
def get_db():
    info_list = [] #db속 정보리스트
    cur.execute("select * from users")
    res = cur.fetchall()
    data = pd.DataFrame.from_records(res)
    id_list = data[0].tolist() #db 속의 아이디리스트
    pw_list = data[1].tolist() #db 속의 비밀번호리스트
    info_list.append(id_list) #정보리스트에 저장 - 아이디리스트는 0번째
    info_list.append(pw_list) #비밀번호 리스트 1번째

    return info_list

#5 회원가입
def signup(message, client):
    signup_message = message.split(',') # ","단위로 신호메세지 내용 구분하기
    id_temp = signup_message[1]  #아이디
    pw_temp = signup_message[2]  #비밀번호
    if id_temp in get_db()[0]: # 아이디 중복체크
        client.send('2'.encode()) #중복된경우 클라이언트에 '2' 전송
    else:
        client.send('1'.encode()) #아닌경우 클라이언트에 '1' 전송
        sql = f"INSERT INTO users (ID,Password) VALUES('{id_temp}','{pw_temp}')" #db에 회원정보추가
        cur.execute(sql)
        conn.commit()
#6 로그인
def user_login(message, client):
    login_info = message.split(',') #로그인정보 구분
    id_temp = login_info[1]
    pw_temp = login_info[2]
    if id_temp in get_db()[0] and pw_temp in get_db()[1]: #아이디,비밀번호 유무확인
        for i in range(len(get_db()[0])):
            if id_temp == get_db()[0][i]:
                id_idx = i #해당 아이디 번호부여
        for i in range(len(get_db()[1])):
            if pw_temp == get_db()[1][i]:
                pw_idx = i #해당 비밀번호 번호부여
        if id_idx == pw_idx: #일치하는 경우
            client.send('1'.encode())
            nicknames.append(id_temp) #접속중인 닉네임 리스트에 추가
            room_dic['temp_room'].append(id_temp) #대기창 목록에 닉네임 추가
        else:
            client.send('2'.encode())
    else: #가입정보가 없는 경우
        client.send('2'.encode())

#7 온라인유저와 채팅방목록 전송
def send_onlineuser_and_chattingroom():
    print(room_dic['temp_room']) #
    onlineusers = '#onlineusers,'
    print('onlineusers : ', onlineusers)
    chattingrooms = ''
    print('chattingrooms : ', chattingrooms)
    for i in room_dic['temp_room']:
        onlineusers += f'{i},'
    for i in room_dic.keys():
        chattingrooms += f'{i},'
    print("여기")
    oac = onlineusers + ';' + chattingrooms
    print('oac', oac)
    broadcast(oac.encode())
    print("nㅠㅠ")

#8 채팅메세지를 대화참여중인 모든 유저에게 전송
def broadcast(message):
    print(clients)
    for i in range(len(clients)):
        print('broad', nicknames[i])
        clients[i].send(message)
        # clients[i].send(message)
        print(message)

#9 채팅방 만들기
def make_room(message):
    make_room_sign = message.split(',')
    room_name = make_room_sign[1] #방이름
    room_user = make_room_sign[2] #방장
    room_dic[room_name] = [room_user] #방리스트에 채팅방과 방장 추가
    idx = nicknames.index(room_user) #방장 번호찾기
    clients[idx].send(f'#joinuser,{room_user} is join;{room_user}'.encode())
    print(room_dic)

#10 채팅방 입장(더블클릭)
def join_room(message):
    room_users = ''
    join_room_sign = message.split(',')
    room_name = join_room_sign[1]
    room_user = join_room_sign[2]
    room_dic[room_name].append(room_user)  #채팅방 리스트에 참여한 유저 추가
    for i in room_dic[room_name]:
        room_users += f'{i},'
    for i in room_dic[room_name]:
        idx = nicknames.index(i)  #방에 있는 모든 유저에게 방입장 알림 메세지 전송
        clients[idx].send(f'#joinuser,{room_user} is join;{room_users}'.encode())

#11 채팅방 나가기
def exit_room(message):
    exit_room_sign = message.split(',')
    room_name = exit_room_sign[1]
    room_user = exit_room_sign[2]
    room_dic[room_name].remove(room_user) #유저 제외
    if room_name != 'temp_room': #유저가 특정방에서 나간경우
        now_users = ''
        if len(room_dic[room_name]) < 1:  #특정방에 남은 유저가 없으면 방 삭제
            del room_dic[room_name]
            del room_pw[room_name]
        else:
            for i in room_dic[room_name]:
                now_users += f'{i},'
            for i in room_dic[room_name]:
                idx = nicknames.index(i) #방에 남아있는 모든 유저에게 방퇴장 알림메세지 전송
                clients[idx].send(f'#exituser,{room_user} out;{now_users[:-1]}'.encode())
#12 초대하기
def invite_room(message):
    invite_message = message.split(',')
    invite_room_name = invite_message[1]
    invite_id_temp = invite_message[2] #초대받은 유저의 아이디
    idx = nicknames.index(invite_id_temp)
    clients[idx].send(f'#inviteuser,{invite_room_name}'.encode()) #초대받은 유저에게 신호메세지 전송

#13 비밀채팅방 만들기
def make_pw_room(message):
    make_room_sign = message.split(',')
    print(make_room_sign)
    room_name = make_room_sign[1]
    room_user = make_room_sign[2]
    room_password = make_room_sign[3]
    room_dic[room_name] = [room_user]
    room_pw[room_name] = [room_password]
    idx = nicknames.index(room_user)
    clients[idx].send(f'#joinuser,{room_user} is join;{room_user}'.encode())
    print(room_dic)
    print(room_pw)

#14 비밀채팅방 입장하기
def join_pw_room(message):
    room_users = ''
    join_room_sign = message.split(',')
    room_name = join_room_sign[1]
    room_user = join_room_sign[2]
    room_password = join_room_sign[3]
    if room_password == room_pw[room_name]:
        room_dic[room_name].append(room_user)
        for i in room_dic[room_name]:
            room_users += f'{i},'
        for i in room_dic[room_name]:
            idx = nicknames.index(i)
            clients[idx].send(f'#joinuser,{room_user} is join;{room_users}'.encode())
    else:
        idx = nicknames.index(room_user)
        clients[idx].send(f'#incorrect'.encode())

#15 중복아이디 체크
def id_check(message, client):
    signup_message = message.split(',')
    id_temp = signup_message[1]
    if id_temp in get_db()[0]:
        client.send('2'.encode())
    else:
        client.send('1'.encode())

#16 채팅-메세지 수신발신
def chatting(message):
    message = message.split('$')
    room_name = message[0]
    message = message[1]
    print(room_dic)
    print('room_name : ', room_name)
    print('message : ', message)
    print('nicknames :', nicknames)
    for i in room_dic[room_name]:
        idx = nicknames.index(i)
        clients[idx].send(message.encode())
        print('i', i)






if __name__ == '__main__':
    print('Server running...')
    receive()
