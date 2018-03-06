# The following libraries need to be installed:
#sudo apt-get install ffmpeg
#pip install moviepy[options]
# Author: Howard Webb
# Date: 2/12/2018
# This program selects pictures within a date range, then selects one per day and converts them to a GIF

try:
    from moviepy.editor import ImageSequenceClip
except NeedDownloadError:
    import imageio
    imageio.plugins.ffmpeg.download()
    from moviepy.editor import ImageSequenceClip    
    
#import cv2
from datetime import datetime
from env import env
from config import config

out_file="plant.gif"

def makeGIF(clips, out_file):
    clips.write_gif(out_file, fps=1)

def getImageClips(pics, speed):
    return ImageSequenceClip(pics, fps=speed)

def resizeClips(clips, wide):
    return clips.resize(width=wide)

def getPics(dir, type, start_date, end_date):    
    prior_day=0
    pics=[]
    for file in sorted(dir):
        if file.endswith(type):
            dt=file.split('_')
#        print file, dt
            if dt[0] > start_date and dt[0] < end_date:
                # get one image per day
                day=dt[0].split('-')
                now=day[2]
#            print now, prior_day
                if now!=prior_day:
#                    print file
                    prior_day = now
                    pics.append(dir+file)
    return pics


def main():
    # Variables to control source and output
    # Start date is the beginning of the trial
    start_date=env['trials'][1]['start_date']
    end_date=str(datetime.now())
    # Source of images
    dir="/home/pi/MPV/pictures/"
    # Image type to select
    type=".jpg"
    # Resize the image to 640x480 (resizing will keep ratio with one dimension specified)
    size=640
    # Output file name (will be in the python directory with this code)
    png_name="plant.gif"
    # Frames per second speed
    speed=2

    print "Get Pics from ", start_date, " to ", end_date
    pics=getPics(dir, type, start_date, end_date)
    print "Get Images"
    if len(pics) == 0:
        print "No Pictures"
        return
#    imgs=getImages(dir, pics)
    clips=getImageClips(pics, speed)
    print "Resize Clips"
    clips=resizeClips(clips, size)
    print "Make Video"
    makeGIF(clips, png_name)

if __name__=="__main__":
    '''Setup for calling from script'''
    main()    
