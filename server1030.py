import socket
import threading
import time
import pymysql
import pandas as pd

Host = '10.10.21.118'
PORT = 5500

conn = pymysql.connect(host='10.10.21.118', port=3306, user='root', password='starDB1234@', db='starDB',
                       charset='utf8')
cur = conn.cursor()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((Host, PORT))
server.listen()
clients = []
nicknames = []
room_dic = {'temp_room': []}
user_id = ''
user_pw = ''


def broadcast(message):
    print(clients)
    for i in range(len(clients)):
        print('broad', nicknames[i])
        clients[i].send(message)


def handle(client):
    while True:
        try:
            print('wait...')
            message = client.recv(1024).decode()
            print(message)
            if not message:
                log_out(client)
                break

            elif '#signup' in message:
                signup(message, client)

            elif '#my_id_pw' in message:
                user_login(message, client)
                continue

            elif '#onlineusers' in message:
                send_onlineuser_and_chattingroom()

            elif '#refresh' in message:
                send_onlineuser_and_chattingroom()

            elif '#makeroom' in message:
                make_room(message)

            elif '#roomjoin' in message:
                join_room(message)
                continue

            elif '#okay' in message:
                join_room(message)

            elif '#exit' in message:
                exit_room(message)

            else:
                chatting(message)

        except:
            log_out(client)
            print('after exit : ', clients, nicknames, room_dic)
            break

def get_db():
    info_list = []
    cur.execute("select * from users")

    res = cur.fetchall()
    print(res)

    data = pd.DataFrame.from_records(res)

    id_list = data[0].tolist()
    pw_list = data[1].tolist()
    info_list.append(id_list)
    info_list.append(pw_list)
    return info_list

def user_login(message, client):
    login_info = message.split(',')
    id_temp = login_info[1]
    pw_temp = login_info[2]
    if id_temp in get_db()[0] and pw_temp in get_db()[1]:
        for i in range(len(get_db()[0])):
            if id_temp == get_db()[0][i]:
                id_idx = i
        for i in range(len(get_db()[1])):
            if pw_temp == get_db()[1][i]:
                pw_idx = i
        if id_idx == pw_idx:
            client.send('1'.encode())
            nicknames.append(id_temp)
            room_dic['temp_room'].append(id_temp)
        else:
            client.send('2'.encode())
    else:
        client.send('2'.encode())



def make_room(message):
    make_room_sign = message.split(',')
    room_name = make_room_sign[1]
    room_user = make_room_sign[2]
    room_dic[room_name] = [room_user]
    idx = nicknames.index(room_user)
    clients[idx].send(f'#joinuser,{room_user} is join;{room_user}'.encode())
    print(room_dic)


def join_room(message):
    room_users = ''
    join_room_sign = message.split(',')
    room_name = join_room_sign[1]
    room_user = join_room_sign[2]
    room_dic[room_name].append(room_user)
    for i in room_dic[room_name]:
        room_users += f'{i},'
    for i in room_dic[room_name]:
        idx = nicknames.index(i)
        clients[idx].send(f'#joinuser,{room_user} is join;{room_users}'.encode())


def exit_room(message):
    exit_room_sign = message.split(',')
    room_name = exit_room_sign[1]
    room_user = exit_room_sign[2]
    room_dic[room_name].remove(room_user)
    if room_name != 'temp_room':
        now_users = ''
        if len(room_dic[room_name]) < 1:
            del room_dic[room_name]
        else:
            for i in room_dic[room_name]:
                now_users += f'{i},'
            for i in room_dic[room_name]:
                idx = nicknames.index(i)
                clients[idx].send(f'#exituser,{room_user} out;{now_users[:-1]}'.encode())


def log_out(client):
    index = clients.index(client)
    nickname = nicknames[index]
    print(nickname, ' out')
    nicknames.remove(nickname)
    for i in room_dic.keys():
        if nickname in room_dic[i]:
            room_dic[i].remove(nickname)
            if room_dic[i] != 'temp_room':
                room_name = room_dic[i]
                print('after logout' , room_name)
    if len(room_name) < 1:
        del room_name
    clients.remove(client)
    client.close()


def chatting(message):
    message = message.split('$')
    room_name = message[0]
    message = message[1]
    print(room_dic)
    print('room_name : ', room_name)
    print('message : ', message)
    print('nicknames :', nicknames)
    for i in room_dic[room_name]:
        print('i', i)
        idx = nicknames.index(i)
        clients[idx].send(message.encode())


def send_onlineuser_and_chattingroom():
    print(room_dic['temp_room'])
    onlineusers = '#onlineusers,'
    chattingrooms = ''
    for i in room_dic['temp_room']:
        onlineusers += f'{i},'
    for i in room_dic.keys():
        chattingrooms += f'{i},'
    oac = onlineusers + ';' + chattingrooms
    broadcast(oac.encode())


def receive():
    while True:
        client, address = server.accept()
        clients.append(client)
        chat_thread = threading.Thread(target=handle, args=(client,))
        chat_thread.start()

def signup(message, client):
    signup_message = message.split(',')
    print("오류4")
    id_temp = signup_message[1]
    pw_temp = signup_message[2]
    print("오류5")
    if id_temp in get_db()[0] or pw_temp in get_db()[1]:
        client.send('2'.encode())
        print("오류6")
    else:
        client.send('1'.encode())
        sql = f"INSERT INTO users (ID,Password) VALUES('{id_temp}','{pw_temp}')"
        cur.execute(sql)
        conn.commit()
        print("오류7")

print('Server running...')
receive()
