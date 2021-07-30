import os
import cv2
import time
import threading

from ffpyplayer.player import MediaPlayer


def __newBufferVideo(file):
    tmp = MediaPlayer(file)
    tmp.set_pause(True)
    return [cv2.VideoCapture(file), tmp, file]


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

    buf[0].release()
    cv2.destroyAllWindows()


def __fetchBuffer(queue, eof, buffer):
    while not eof or queue:
        if queue and len(buffer) < 2: buffer.append(__newBufferVideo(queue.pop(0)))
        time.sleep(0.5)


def player(file, eof, queue):
    buffer = []
    fetchingThread = threading.Thread(target=__fetchBuffer, args=[queue, eof, buffer])
    fetchingThread.start()

    while True:
        if (not eof or queue) and not buffer:
            time.sleep(0.1)
            continue

        buf = buffer.pop(0)
        buf[1].set_pause(False)

        while True:
            grabbed, frame = buf[0].read()
            audio  , val   = buf[1].get_frame()

            if not grabbed: break
            if cv2.waitKey(1) & 0xFF == ord("q"): break

            cv2.imshow(file, frame)

            if val == "eof": break
            elif audio is None: time.sleep(0.005)
            else:
                img, t = audio
                time.sleep(val)

        # os.remove(buf[2]) # remove the played file from clinet
    
        buf[0].release()
        if not queue and eof and not buffer: break

    fetchingThread.join()
    cv2.destroyAllWindows()
