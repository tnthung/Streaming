import os
import time
import json
import split
import threading

import TCP.Server as Server


myServer = Server.Server()


@myServer.addClinetFunction("Hello")
def sayHello(conn, msg=""):
    myServer.send(conn, b"Hi " + msg.encode() + b"!")

@myServer.addClinetFunction("play")
def playVideo(conn, video=""):
    if not os.path.exists(video): 
        myServer.send(conn, b"No video found")
        return

    fileStatus = {}
    myServer.send(conn, b"Start playing " + video.encode())
    index = 1
    flag = [
        0, # total part
        0, # current have
    ]

    if os.path.exists("Video.json"):
        with open("Video.json", "r") as f: fileStatus = json.load(f)

    if (tmp := fileStatus.get(video, None)) is not None: flag = tmp
    else: threading.Thread(target=split.splitVideo, args=(video, flag)).start()

    while True:
        if flag[1] >= 1 and index <= flag[1] :
            fileStatus[video] = [flag[0]] * 2
            myServer.recv(conn)
            
            with open(video[:-4]+f"{index}.mp4", "rb") as f:
                myServer.send(conn, f.read())
                index += 1
            # os.remove(command[1][:-4]+f"{index}.mp4")

            if flag[0] == flag[1] == index-1:
                break

        time.sleep(1)

    with open("Video.json", "w") as f: json.dump(fileStatus, f)

    myServer.recv(conn)
    myServer.send(conn, b"eof")

@myServer.addServerFunction("QUIT")
def quitServer(*args):
    myServer.end()

@myServer.addServerFunction("list")
def listClinet(*args):
    conn = myServer.connections

    print(f"{len(conn)}/{myServer.maxConnection} connections.\n")

    for i, j in enumerate(conn): print(f"{i+1}.", j[1])


myServer.start()
