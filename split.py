from moviepy.editor import *


def splitVideo(inputFile, duration=30):
    video = VideoFileClip(inputFile+".mp4")
    length = video.duration

    time = 0
    index = 0
    while time+duration < length:
        video.subclip(time, time+duration).write_videofile(f"{inputFile}{index:3}.mp4")
        time += duration
        index += 1
    
    else:
        video.subclip(time, length).write_videofile(f"{inputFile}{index:3}.mp4")

    video.close()


if __name__ == '__main__':
    splitVideo("testVideo")
