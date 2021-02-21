#!/usr/bin/python
from Video import Video

video = Video('video.mp4')

### to see how it looks like
# video.stream = video.stream.trim(start_frame=0, end_frame=60)

video.addLogo("tub.png", position= "BOTTOM_LEFT", scale = 0.1)
video.addLogo("intcdc_logo.png", position= "BOTTOM_MIDDLE", scale = 0.1)
video.addLogo("mpi.png", position= "BOTTOM_RIGHT", scale = 0.1)

video.output('out.mp4')
