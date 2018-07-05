# The following libraries need to be installed:
#sudo apt-get install ffmpeg
#pip install moviepy[options]
# Author: Howard Webb
# Date: 2/12/2018
# This program selects pictures within a date range, then selects one per day and converts them to a GIF

from moviepy.editor import ImageSequenceClip 
import cv2
import os
from datetime import datetime
from env import env

def makeGIF(clips, out_file):
    clips.write_gif(out_file, fps=1)

def getImageClips(pics, speed):
    return ImageSequenceClip(pics, fps=speed)

def resizeClips(clips, wide):
    return clips.resize(width=wide)

def getPics(dir, type, start_date, end_date, test=False):
    if test:
        print "Getting Pics"
    prior_day=0
    pics=[]
    for file in sorted(os.listdir(dir)):
        if file.endswith(type):
            dt=file.split('_')
#            if test:
#                print file, dt

            if dt[0] > start_date and dt[0] < end_date:
                # get one image per day
                day=dt[0].split('-')
                now=day[2]
#            print now, prior_day
                if now!=prior_day:
                    if test:
                        print file, os.stat(dir + file).st_size
                    prior_day = now
                    pics.append(dir+file)
    return pics


def main(test=False):
    # Variables to control source and output
    start_date=env["trials"][1]["start_date"]
    end_date=str(datetime.now())
    # Source of images
    dir="/home/pi/MVP/pictures_R/"
    # Image type to select
    type=".jpg"
    # Resize the image to 640x480 (resizing will keep ratio with one dimension specified)
    size=640
    # Output file name (will be in the python directory with this code)
    png_name="plant.gif"
    # Frames per second speed
    speed=2
    if test:
        print "Get Pics from ", dir, " ", start_date, " to ", end_date
    pics=getPics(dir, type, start_date, end_date, test)
    print "Get Images"
#    imgs=getImages(dir, pics)
    clips=getImageClips(pics, speed)
    print "Resize Clips"
    clips=resizeClips(clips, size)
    print "Make Video"
    makeGIF(clips, png_name)

if __name__=="__main__":
    main()    
