#!/usr/bin/python
from src.Video import Video

video = Video('data/animation_well.mp4')

### to see how it looks like
# video.stream = video.stream.trim(start_frame=0, end_frame=200)

video.addLogo("logos/tub.png", position= "BOTTOM_LEFT", scale = 0.1)
video.addLogo("logos/EXC_IntCDC_Logo.png", position= "BOTTOM_MIDDLE", scale = 0.1)
video.addLogo("logos/mpi.png", position= "BOTTOM_RIGHT", scale = 0.1)

video.output('data/out.mp4')
