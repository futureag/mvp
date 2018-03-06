#!/bin/bash

# Once a day create the gif file and move it to the web directory

python_dir="/home/pi/MVP/python/"

#Create the GIF file
python "$python_dir"img2gif.py

#Move the gif to the web directory
mv -f /home/pi/plant.gif /home/pi/MVP/web/plant.gif