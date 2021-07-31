import time
import player
import threading

import TCP.Client as Client


myClient = Client.Client()


@myClient.addMode("Hello")
def sayHello(conn, command):
    conn.sendall(command.bytes)
    myClient.announce(conn.recv(1024), As="Server")

@myClient.addMode("QUIT")
def quitServer(*args):
    myClient.end()

@myClient.addMode("play")
def play(conn, command):
    conn.sendall(command.bytes)
    respond = conn.recv(1024)
    myClient.announce(respond, As="Server")

    if respond == b"No video found": return

    index = 1
    isSent = True
    queue = []
    eof = []

    playerThread = threading.Thread(target=player.player, args=[command.split[1], eof, queue])
    playerThread.start()

    conn.sendall(b"req")
    while 1:
        if isSent:
            isSent = False
            file = f"{index}.mp4"
            data = conn.recv(5*1024*1024)

            if data == b"eof": 
                eof.append(1)
                break

            with open(file, "wb") as f:
                f.write(data)
                queue.append(file)
                index += 1

        else:
            time.sleep(0.5)

        if len(queue) < 1:
            conn.sendall(b"req")
            isSent = True

    playerThread.join()


myClient.start()
