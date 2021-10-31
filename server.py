#!/usr/bin/env python3
import os
import socket
import threading
import sys
import signal

PORT = 2000
PORT1 = 3000
SERVER = '127.0.0.1'
FORMAT = 'utf-8'
SERVER_DATA_PATH = "server_data"
CLIENT_DATA_PATH = "client_data"
usernames = {}


def func(char, client):
    msg = ""
    while True:
        txt = client.recv(1).decode(FORMAT)
        if txt == char: break
        msg += txt
    return msg

def sig_handler(sig, frame):
    print('\nSIGINT signal received!')
    sys.exit(0)
signal.signal(signal.SIGINT, sig_handler)

def handle(client, address):
    with client:
        conn = True
        while conn:
            msg = client.recv(1024).decode(FORMAT)
            cmd1 = msg.split()
            cmd = cmd1[0]
            if cmd == "DISCONNECT":
                try:
                    client.send("OK".encode(FORMAT))
                    for i in usernames:
                        print(i)
                        if usernames[i] == address[0]:
                            usernames.pop(i)
                            addr = usernames.pop(i)
                            conn = False
                            print(f"Client {usernames[i]} disconnected!")
                    with server1:
                        server1.connect((addr,PORT1))
                        server1.send("DISCONNECT\n".encode(FORMAT))
                        break
                except:
                    print("Failed to disconnect!")
            elif cmd == "LU":
                Usernames = ""
                for i in usernames:
                    Usernames += i + " "
                Usernames += "\n"
                client.send(Usernames.encode(FORMAT))   
            elif cmd == "LF":
                files = os.listdir(SERVER_DATA_PATH)
                send_data = ""
                if len(files) == 0:
                    send_data += "The server directory is empty."
                else:
                    send_data += " ".join(f for f in files)
                send_data += "\n"
                client.send(send_data.encode(FORMAT))
            elif cmd == "READ":
                name = cmd1[1]
                files = os.listdir(SERVER_DATA_PATH)
                if name not in files:
                    client.send("Server does not contain this file!".encode(FORMAT))
                else:
                    client.send("OK".encode(FORMAT))
                    filepath = os.path.join(SERVER_DATA_PATH, name) 
                    with open(filepath, "r") as f:
                        text = f.read()
                    size = os.path.getsize(filepath)
                    client.send(f"{size} {text}".encode(FORMAT))
            elif cmd == "WRITE":
                name = cmd1[1]
                files = os.listdir(SERVER_DATA_PATH)
                if name in files:
                    client.send("Server already contains this file!".encode(FORMAT))
                else:
                    client.send("OK".encode(FORMAT))
                    filesize = func(' ', client)
                    content = client.recv(int(filesize)).decode(FORMAT)
                    filepath = os.path.join(SERVER_DATA_PATH, name) 
                    with open(filepath, "w") as f:
                        f.write(content)               
            elif cmd == "OVERREAD":
                name = cmd1[1]
                files = os.listdir(SERVER_DATA_PATH)
                if name not in files:
                    client.send("Server does not contain this file!".encode(FORMAT))
                else:
                    client.send("OK".encode(FORMAT))
                    filepath = os.path.join(SERVER_DATA_PATH, name) 
                    with open(filepath, "r") as f:
                        text = f.read()
                    size = os.path.getsize(filepath)
                    client.send(f"{size} {text}".encode(FORMAT))
            elif cmd == "OVERWRITE":
                name = cmd1[1]
                client.send("OK".encode(FORMAT))
                filesize = func(' ', client)
                content = client.recv(int(filesize)).decode(FORMAT)
                filepath = os.path.join(SERVER_DATA_PATH, name) 
                with open(filepath, "w") as f:
                    f.write(content)
            elif cmd == "APPEND":
                name = cmd1[1]
                files = os.listdir(SERVER_DATA_PATH)
                if name in files:
                    client.send("OK".encode(FORMAT))
                    filesize = func(' ', client)
                    text = client.recv(int(filesize)).decode(FORMAT)
                    filepath = os.path.join(SERVER_DATA_PATH, name) 
                    with open(filepath, "a") as f:
                        f.write(text)
                else:
                    client.send("Server does not contain this file!".encode(FORMAT))                                
            elif len(cmd1) == 3 and cmd == "APPENDFILE":
                server_file = cmd1[2]
                files = os.listdir(SERVER_DATA_PATH)
                if server_file in files:
                    client.send("OK".encode(FORMAT))
                    filesize = func(' ', client)
                    text = client.recv(int(filesize)).decode(FORMAT)
                    filepath = os.path.join(SERVER_DATA_PATH, server_file)
                    with open(filepath, "a") as f:
                        f.write(text)
                else:
                    client.send("Server does not contain this file!".encode(FORMAT))
            elif len(cmd1) >= 3 and cmd == "MESSAGE":
                if cmd1[1] in usernames:
                    client.send("OK\n".encode(FORMAT))
                    size = int(func(' ', client))
                    msg = client.recv(size).decode(FORMAT)
                    with server1:
                        server1.connect((usernames[cmd1[1]], PORT1))
                        server1.send(f"MESSAGE\n {size} {msg}".encode(FORMAT))
                else:
                    client.send(f"{cmd1[1]} is not online!")
            else:
                client.send("Incorrect command".encode(FORMAT))
                client.close()
                break
    client.close()
    server1.close()


try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen()
    print("Server is listening...")
    while True:
        client, address = server.accept()
        username = client.recv(1024).decode(FORMAT).split()[1]
        if username not in usernames:
            client.send("OK\n".encode(FORMAT))
            usernames[username] = address
            print(f"Connected {username} with address {str(address)}")
        else:
            client.send("This user already exists!".encode(FORMAT))

        handle_thread = threading.Thread(target=handle, args=(client, address))
        handle_thread.start()
except KeyboardInterrupt:
    for i in usernames:
        with server1:
            server1.connect(address, PORT1)
            server1.send("DISCONNECT\n".encode(FORMAT))
            usernames.pop(i)
    print('Server closed')
    server.close()