import time
import socket
import player
import threading


IP = "127.0.0.1"
PORT = 8080

CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CONN.connect((IP, PORT))

# tell if connected
print(CONN.recv(1024))

while True:
    command = input(": ")
    _command = command.split(" ")

    CONN.sendall(command.encode()) # send command
    if command == "quit": break

    respond = CONN.recv(1024) # recv respond
    print(f"[Server] {respond}")

    if _command[0] == "play" and respond == b"File found":
        # length = CONN.recv(1024) # fetch the sections' length
        index = 1
        isSent = True
        queue = []
        eof = []

        playerThread = threading.Thread(target=player.player, args=[_command[1], eof, queue])
        playerThread.start()

        CONN.sendall(b"req")
        while 1:
            if isSent:
                isSent = False
                file = f"{index}.mp4"
                data = CONN.recv(5*1024*1024)

                if data == b"eof": 
                    eof.append(1)
                    break

                with open(file, "wb") as f:
                    f.write(data)
                    queue.append(file)
                    index += 1

            else:
                time.sleep(0.5)

            if len(queue) < 3:
                CONN.sendall(b"req")
                isSent = True

        playerThread.join()

