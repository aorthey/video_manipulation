#!/usr/bin/python
from src.Video import Video

video = Video('data/video.mp4')

### to see how it looks like
video.addTitleScreen("logos/introscreen.png", duration=8)
video.addAudio("sounds/angelic-swell.wav", duration=8)
video.stream = video.stream.trim(duration=8 + 4)
video.addLogo("logos/tub.png", position= "BOTTOM_LEFT", scale = 0.1)
video.addLogo("logos/intcdc_logo.png", position= "BOTTOM_MIDDLE", scale = 0.1)
video.addLogo("logos/mpi.png", position= "BOTTOM_RIGHT", scale = 0.1)

video.output('data/out.mp4')
