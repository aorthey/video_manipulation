#!/usr/bin/python
from src.Video import Video

durationTitleScreen = 8
scaleLogos = 0.15

video = Video('data/video.mp4')

video.addTitleScreen("logos/introscreen.png", duration=durationTitleScreen)
video.addAudio("sounds/angelic-swell.wav", duration=8)

video.stream = video.stream.trim(duration=durationTitleScreen + 6)

video.addLogo("logos/tub.png", position= "BOTTOM_LEFT", \
    scale = scaleLogos, duration=durationTitleScreen)
video.addLogo("logos/EXC_IntCDC_Logo.png", position= "BOTTOM_MIDDLE", \
    scale = scaleLogos, duration=durationTitleScreen)
video.addLogo("logos/mpi.png", position= "BOTTOM_RIGHT", \
    scale = scaleLogos, duration=durationTitleScreen)

video.output('data/out.mp4')
