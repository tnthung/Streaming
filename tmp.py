from math import trunc
import os
import cv2
import time
import threading

from ffpyplayer.player import MediaPlayer


def __newBufferVideo(file):
    return [cv2.VideoCapture(file), MediaPlayer(file)]


def __playSingleVideo(file):
    buf = __newBufferVideo(file)

    while True:
        grabbed, frame = buf[0].read()
        audio  , val   = buf[1].get_frame()

        if not grabbed: break
        if cv2.waitKey(1) & 0xFF == ord("q"): break

        cv2.imshow(file, frame)

        if val == "eof": break
        elif audio is None: time.sleep(0.01)
        else:
            img, t = audio
            time.sleep(val)


def player(file, eof, queue):
    buffer = []

    buffer.append(__newBufferVideo(queue[0]))

    while True:
        buf = buffer.pop(0)

        while True:
            grabbed, frame = buf[0].read()
            audio  , val   = buf[1].get_frame()

            if not grabbed: break
            if cv2.waitKey(1) & 0xFF == ord("q"): break

            cv2.imshow(file, frame)

            if val == "eof": break
            elif audio is None: time.sleep(0.01)
            else:
                img, t = audio
                time.sleep(val)

        queue.pop(0)

        if len(queue) > 1: buffer.append(__newBufferVideo(queue[0]))
        elif eof: break


if __name__ == '__main__':
    # __playSingleVideo('5.mp4')

    t = threading.Thread(target=player, args=["testVideo", [1], [f"{i}.mp4" for i in range(1, 14)]])
    t.start()

    t.join()
