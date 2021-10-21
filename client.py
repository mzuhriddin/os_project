import socket

FORMAT = 'utf-8'
PORT = 2021
SERVER = socket.gethostbyname('localhost')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


stat = True
while stat:
    msg = input("Enter a command: ")
    conn = False
    cmd1 = msg.split()
    cmd = cmd1[0]
    if (len(cmd1) == 3 and cmd == 'connect'):
        print(f"Client {cmd1[1]} connected!")
        client.connect((SERVER, PORT))
        client.send(f"CONNECT {cmd1[1]}".encode(FORMAT))
        conn = True 
        while conn:
            msg = input("Enter a command: ")
            cmd1 = msg.split()
            cmd = cmd1[0]
            if len(cmd1) == 1:
                if cmd == 'disconnect':
                    client.send("DISCONNECT".encode(FORMAT))
                    response = client.recv(1024).decode(FORMAT)
                    if response == 'disconnect':
                        print('Disconnected')
                        conn = False
                    else:
                        print("Failed to disconnect!")
                elif cmd == 'quit':
                    client.send("QUIT".encode(FORMAT))
                    print("Client is quitting!")
                    stat = False
                    break
                elif cmd == 'lu':
                    
                    response = client.recv(1024).decode(FORMAT)
                    print(response)
                elif cmd == 'lf':
                    client.send("LF".encode(FORMAT))
                    response = client.recv(1024).decode(FORMAT)
                    print(response)
                else:
                    print("Wrong command! Try again.")
            elif len(cmd1 == 2):
                if cmd == "read":
                    client.send(f"READ {cmd1[1]}".encode(FORMAT))
                    response = client.recv(1024).decode(FORMAT)
                    print(response)
                elif cmd == "write":
                    client.send(f"WRITE {cmd1[1]}".encode(FORMAT))
                    response = client.recv(1024).decode(FORMAT)
                    print(response)
                elif cmd == "overread":
                    client.send(f"OVERREAD {cmd1[1]}".encode(FORMAT))
                    response = client.recv(1024).decode(FORMAT)
                    print(response)
                elif cmd == "overwrite":
                    client.send(f"OVERWRITE {cmd1[1]}".encode(FORMAT))
                    response = client.recv(1024).decode(FORMAT)
                    print(response)
                else:
                    print("Wrong command! Try again.")
            elif cmd == "appendfile" and len(cmd1) == 3:
                client.send(f"APPENDFILE {cmd1[1]} {cmd1[2]}".encode(FORMAT))
                response = client.recv(1024).decode(FORMAT)
                print(response)
            elif cmd == "send" and len(cmd1) >= 3:
                if cmd1[1] == 'not_online':
                    print('Error: User is not online')
                    continue
                msg = msg[msg.find('“') + 1:msg.find('”')]
                send = 'MESSAGE {}\n{} {}'.format(cmd1[1], len(msg), msg)
                print(send)
            elif cmd == "append" and len(cmd1) >= 3:
                    print(f"APPEND {cmd1[-1]}")
                    print("NUMBER_OF_BYTES FILE_CONTENT")
            else:
                print("Wrong command! Try another pattern.")
    elif cmd == 'quit':
        print("Client is quitting!")
        stat = False
    else:
        print("Enter only connect or quit.")
