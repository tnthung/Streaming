import time
import player
import threading

import TCP.Client as Client


myClient = Client.Client()


@myClient.addMode("Hello")
def sayHello(command):
    myClient.sendObj(command)
    myClient.announce(myClient.recv(1024), "Server")

@myClient.addMode("QUIT")
def quitServer(*args):
    myClient.end()

@myClient.addMode("play")
def play(command):
    myClient.sendObj(command)
    if myClient.announceRespond() == "No video found": return

    index = 1
    isSent = True
    queue = []
    eof = []

    playerThread = threading.Thread(target=player.player, args=[command.split[1], eof, queue])
    playerThread.start()

    myClient.send(b"req")
    while 1:
        if isSent:
            isSent = False
            file = f"{index}.mp4"
            data = myClient.recv(5*1024*1024)

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
            myClient.send(b"req")
            isSent = True

    playerThread.join()


myClient.start()
