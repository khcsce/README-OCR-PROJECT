#!/bin/bash

#Take picture withe fswebcam 
fswebcam -r 1280x720 --no-banner image1.jpg

#Call Image Publisher to send image 
python Image_publisher.py 