#!/usr/bin/python
import ffmpeg
from src.Video import Video
from PIL import Image
import sys,os

filename = "data/zoomChrisMavrogiannis.mp4"

fileWOextension = os.path.splitext(filename)[0]
fileTitle = fileWOextension+'TitleScreen.mp4'
fileAnnotated = fileWOextension+'Annotated.mp4'
fileOutput = fileWOextension+'Output.mp4'

## generate title screen
videoTitle = Video(filename,ss=0,duration=0)
videoTitle.addTitleScreen('logos/rc.png', duration=6)
videoTitle.addAudio('sounds/angelic-swell.wav')
videoTitle.stream = videoTitle.stream.trim(duration=6)
videoTitle.output(fileTitle)

### generate overlay text

#video = Video(filename)
########################################################################
###### CUSTOM SETTINGS BASED ON SPEAKER ####
#video.addSpecialText("Andreas Orthey", tStart=7, tEnd=15)
#video.addSpecialText("Chris Mavrogiannis", tStart=71, tEnd=75)
########################################################################
#video.output(fileAnnotated)

#### concat videos
cmd = "ffmpeg -i %s -i %s -filter_complex \'concat=n=2:v=1:a=1[a]\' \
    -map \'[a]\' -codec:a libmp3lame -b:a 256k %s"%(fileTitle, fileAnnotated, fileOutput)
os.system(cmd)
