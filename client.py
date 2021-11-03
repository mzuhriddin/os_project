#!/usr/bin/env python3
import os
import socket
from threading import *
import re


FORMAT = 'ascii'
SERVER = "127.0.0.1"
PORT = 2021
PORT1 = 2022
SERVER_DATA_PATH = "server_data"
CLIENT_DATA_PATH = "client_data"
stat  = True
conn = True
mutex = Lock()

def func(char, client):
    msg = ""
    while True:
        content = client.recv(1).decode(FORMAT)
        if content == char: break
        msg += content
    return msg
def sending(client):
    global stat, conn
    while conn:
        msg = input("Enter a command: ")
        cmd2 = msg.split()
        com = cmd2[0]
        if com == 'disconnect':
            client.send("DISCONNECT".encode(FORMAT))
            response = client.recv(1024).decode(FORMAT)
            if response == 'OK':
                mutex.acquire()
                print('Disconnecting')
                client.close()
                conn = False
                mutex.release()
            else:
                print("Failed to disconnect!")
        elif com == 'lu':
            client.send("LU".encode(FORMAT))
            response = client.recv(1024).decode(FORMAT)
            mutex.acquire()
            print(response)
            mutex.release()                        
        elif com == 'lf':
            client.send("LF".encode(FORMAT))
            response = client.recv(1024).decode(FORMAT)
            mutex.acquire()
            print(response)
            mutex.release() 
        elif com == "read":
            client.send(f"READ {cmd2[1]}".encode(FORMAT))
            print(client.recv(1024).decode(FORMAT))
            files = os.listdir(CLIENT_DATA_PATH)
            if cmd2[1] in files:
                print("Client already contains this file!")
            else:
                filesize = func(' ', client)
                content = client.recv(int(filesize)).decode(FORMAT)
                filepath = os.path.join(CLIENT_DATA_PATH, cmd2[1]) 
                with open(filepath, "w") as f:
                    f.write(content)
                print("File uploaded")                      
        elif com == "write":
            files = os.listdir(CLIENT_DATA_PATH)
            if cmd2[1] not in files:
                client.send("Client does not contain this file!".encode(FORMAT))
            else:
                client.send(f"WRITE {cmd2[1]}".encode(FORMAT))
            a = client.recv(1024).decode(FORMAT)
            print(a)
            if a == "OK":
                path = os.path.join(CLIENT_DATA_PATH, cmd2[1])
                with open(f"{path}", "r") as f:
                    text = f.read()
                size = os.path.getsize(path)
                client.send(f"{size} {text}".encode(FORMAT))
        elif com == "overread":
            client.send(f"OVERREAD {cmd2[1]}".encode(FORMAT))
            print(client.recv(1024).decode(FORMAT))
            filesize = func(' ', client)
            content = client.recv(int(filesize)).decode(FORMAT)
            filepath = os.path.join(CLIENT_DATA_PATH, cmd2[1]) 
            with open(filepath, "w") as f:
                f.write(content)
            print("File replaced")      
        elif com == "overwrite":
            files = os.listdir(CLIENT_DATA_PATH)
            if cmd2[1] not in files:
                client.send("Client does not contain this file!".encode(FORMAT))
            else:
                client.send(f"OVERWRITE {cmd2[1]}".encode(FORMAT))
            a = client.recv(1024).decode(FORMAT)
            print(a)
            if a == "OK":
                path = os.path.join(CLIENT_DATA_PATH, cmd2[1])
                with open(f"{path}", "r") as f:
                    text = f.read()
                size = os.path.getsize(path)
                client.send(f"{size} {text}".encode(FORMAT))
        
        elif com == "append" and len(cmd2) >= 3:
            client.send(f"APPEND {cmd2[-1]}".encode(FORMAT))
            a = client.recv(1024).decode(FORMAT)
            print(a)
            if a == "OK":
                txt = re.findall('"([^"]*)"', msg)
                text = ""
                for i in range(len(txt)):
                    text += txt[i]
                size = len(text)
                client.send(f"{size} {text}".encode(FORMAT))
                response = client.recv(1024).decode(FORMAT)
                print(response)
        elif com == "appendfile" and len(cmd2) == 3:
            files = os.listdir(CLIENT_DATA_PATH)
            if cmd2[1] not in files:
                client.send("Client does not contain this file!".encode(FORMAT))
            else:
                client.send(f"APPENDFILE {cmd2[1]} {cmd2[2]}".encode(FORMAT))
            a = client.recv(1024).decode(FORMAT)
            print(a)
            if a == "OK":
                path = os.path.join(CLIENT_DATA_PATH, cmd2[1])
                with open(f"{path}", "r") as f:
                    text = f.read()
                size = os.path.getsize(path)
                client.send(f"{size} {text}".encode(FORMAT))
        elif com == "send" and len(cmd2) >= 3:
            txt = re.findall('"([^"]*)"', msg)
            size = len(txt)
            client.send(f"MESSAGE {cmd2[1]}\n {size} {txt}".encode(FORMAT))
            response = client.recv(1024).decode(FORMAT)
            print(response)
        else:
            print("Wrong command! Try another pattern.")
        

def receiving():
    global conn, SERVER
    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server1.bind((SERVER, PORT1))
    server1.listen(5)
    while True:
        client1, address1 = server1.accept()
        with client1:
            cmd = func('\n', client1)

            if cmd == "DISCONNECT":
                conn = False
                mutex.acquire()
                print("Disconnected")
                mutex.release()
                server1.close()
            elif cmd == "MESSAGE":
                size = int(func(' ', client1))  
                msg = client1.recv(size).decode(FORMAT)
                mutex.acquire()
                print(f"Received message: {msg}")
                mutex.release()
            else: continue
    
while stat:
    mutex.acquire()
    conmsg = input("Enter connect or quit: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cmd1 = conmsg.split()
    cmd = cmd1[0]
    
    if (len(cmd1) == 3 and cmd == 'connect'):
        HOST = cmd1[2]
        try:
            client.connect((HOST, PORT))
            client.send(f"CONNECT {cmd1[1]}".encode(FORMAT))
            conn = True
            print(client.recv(1024).decode(FORMAT))
        except socket.error as e:
            print(e)
            client.close()
            mutex.release()
            break
        
        sending_thread = Thread(target=sending, args=(client, ))
        receiving_thread = Thread(target=receiving)

        sending_thread.start()
        receiving_thread.start()

        sending_thread.join()
        receiving_thread.join()

        client.close()
    elif cmd == "quit":
        stat = False
    else:
        print("First type only connect or quit!")
