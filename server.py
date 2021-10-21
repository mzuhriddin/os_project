import socket

PORT = 2021
SERVER = socket.gethostbyname("localhost")
FORMAT = 'utf-8'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
server.listen()


    
while True:
    print("Server is listening...")
    client, address = server.accept()
    username = client.recv(1024).decode(FORMAT).split()[1]
    print(f"Connected {username} with address {str(address)}")

    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            cmd1 = msg.split()
            cmd = cmd1[0]
            
        except:
            print("Error occured")
            break
        if len(cmd1) == 1:
            if cmd == "DISCONNECT":
                client.send("disconnect".encode(FORMAT))
                print(f"Client {username} disconnected!")
                client.close()
                break
            elif cmd == "LU":
                client.send("List of users".encode(FORMAT))
            elif cmd == "QUIT":
                print(f"Client {username} quitted!")
            elif cmd == "LF":
                client.send("List of files".encode(FORMAT))
            else:
                client.send("Incorrect command".encode(FORMAT))
                client.close()
                break
        elif len(cmd1) == 2:
            if cmd == "READ":
                client.send(" ".encode(FORMAT))
            if cmd == "WRITE":
                client.send(" ".encode(FORMAT))
            if cmd == "OVERREAD":
                client.send(" ".encode(FORMAT))
            if cmd == "OVERWRITE":
                client.send(" ".encode(FORMAT))
            if cmd == "APPEND":
                client.send(" ".encode(FORMAT))
        elif len(cmd1) == 3 and cmd == "APPENDFILE":
            client.send(" ".encode(FORMAT))
        elif len(cmd1) >= 4 and cmd == "MESSAGE":
            client.send(" ".encode(FORMAT))
        else:
            client.send("Incorrect command".encode(FORMAT))
            client.close()
            break
