from moviepy.editor import *
from math import ceil


def splitVideo(inputFile, returnList, duration=15):
    video = VideoFileClip(inputFile)
    length = video.duration

    if returnList is not None: returnList[0] = ceil(length/duration)

    time = 0
    index = 1
    while time+duration < length:
        video.subclip(time, time+duration).write_videofile(f"{inputFile[:-4]}{index}.mp4")
        if returnList is not None: returnList[1] = index
        time += duration
        index += 1
    
    else:
        video.subclip(time, length).write_videofile(f"{inputFile[:-4]}{index}.mp4")
        returnList[1] = index

    video.close()


if __name__ == '__main__':
    splitVideo("testVideo")
