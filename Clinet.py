import time
import player
import threading

import TCP.Clinet as Clinet


myClinet = Clinet.Clinet()


@myClinet.addMode("Hello")
def sayHello(conn, command):
    conn.sendall(command.bytes)
    myClinet.announce(conn.recv(1024), As="Server")

@myClinet.addMode("QUIT")
def quitServer(*args):
    myClinet.end()

@myClinet.addMode("play")
def play(conn, command):
    conn.sendall(command.bytes)
    respond = conn.recv(1024)
    myClinet.announce(respond, As="Server")

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


myClinet.start()
