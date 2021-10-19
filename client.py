
def write():
    stat = True
    while stat:
        conn = False
        msg = input("Enter a command: ")
        cmd1 = msg.split()
        cmd = cmd1[0]

        if (len(cmd1) == 3 and cmd == 'connect'):
            print(f"Client {cmd1[1]} connected!")
            conn = True
        elif cmd == 'quit':
            print("")
            stat = False
        else:
            print("Enter connect or quit.")
    
    while conn:
        msg = input("Enter a command: ")
        cmd1 = msg.split()
        cmd = cmd1[0]
        if len(cmd1) == 1:
            if cmd == 'disconnect':
                print('Disconnected')
                conn = False

            elif cmd == 'quit':
                stat = False
                conn = False

            elif cmd == 'lu':
                print('LU')

            elif cmd == 'lf':
                print('LF')
            else:
                print("Wrong command! Try again.")
            
        elif len(cmd1 == 2):
            if cmd == "read":
                    print(f"READ {cmd1[1]}")

            elif cmd == "write":
                    print(f"WRITE {cmd1[1]}")

            elif cmd == "overread":
                print(f"OVERREAD {cmd1[1]}")

            elif cmd == "overwrite":
                print(f"OVERWRITE {cmd1[1]}")

            else:
                print("Wrong command! Try again.")

        elif cmd == "appendfile" and len(cmd1) == 3:

            print(f"APPENDFILE {cmd1[1]} {cmd1[2]}")

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


write()