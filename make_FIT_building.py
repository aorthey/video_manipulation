#!/usr/bin/python
from src.Video import Video

import ffmpeg

fname = 'data/FIT_building.mp4'
video = Video(fname)

# video.stream = video.stream.trim(start_frame=0, end_frame=100)

video.addAudio("sounds/time/HansZimmer3m10s.mp3", \
    duration=video.duration, fade_in=2, fade_out=1)

scaleLogo = 0.12
video.addLogos( ["logos/mpi.png", "logos/EXC_IntCDC_Logo.png", \
        "logos/UniStuttgart.png", "logos/tub_light.png"], scale = scaleLogo)

video.output('data/FIT_building_annotated.mp4')
