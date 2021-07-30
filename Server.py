import socket
import os
import threading
import time
import split


IP = "127.0.0.1"
PORT = 8080

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((IP, PORT))
serverSocket.listen(10)

print(f"Listening {IP=}, {PORT=}")


alive = True
CONN, ADDR = serverSocket.accept()

# tell connected
print("[System] Connected")
CONN.sendall(b"Connected")


while alive:
    command = CONN.recv(1024).decode().split(" ") # catch command
    print(f"[Clinet] {command=}")

    if command[0] == "play":
        if len(command) != 2:
            CONN.sendall(b"Wrong command")

        elif not os.path.exists(command[1]):
            CONN.sendall(b"File not found")

        else:
            CONN.sendall(b"File found")
            index = 1
            flag = [
                0, # total part
                0, # current have
            ]

            threading.Thread(target=split.splitVideo, args=(command[1], flag)).start()
            # split.splitVideo(command[1], returnList=flag)

            '''
            while True: # tell clinet the sections' length
                if flag[0] > 0:
                    CONN.sendall(str(flag[0]).encode())
                    break
            
                time.sleep(0.5)
            '''

            while True:
                if flag[1] >= 1 and index <= flag[1] :
                    CONN.recv(1024)
                    
                    with open(command[1][:-4]+f"{index}.mp4", "rb") as f:
                        CONN.sendall(f.read())
                        index += 1
                    # os.remove(command[1][:-4]+f"{index}.mp4")

                    if flag[0] == flag[1] == index-1:
                        break

                time.sleep(0.5)

            CONN.recv(1024)
            CONN.sendall(b"eof")

    elif command[0] == "Hello":
        CONN.sendall(b"Hi there")

    elif command[0] == "quit":
        alive = False


CONN.close()

