#!/usr/bin/python
from src.Video import Video

# video = Video('data/animation_well.mp4')

### to see how it looks like
# video.stream = video.stream.trim(start_frame=0, end_frame=200)

#ffmpeg -ss 00:02:25 -i HansZimmerTimeFull.mp3 -t 83 -b:a 192k -c:a libmp3lame

import ffmpeg

fname = 'data/animation_well.mp4'
video = Video(fname)

video.addAudio("sounds/time/HansZimmerTime83s.mp3", \
    duration=video.duration, fade_in=2, fade_out=10)

scaleLogo = 0.12
video.addLogos( ["logos/mpi.png", "logos/EXC_IntCDC_Logo.png", \
        "logos/UniStuttgart.png", "logos/tub_light.png"], scale = scaleLogo)

video.output('data/animation_well_time2.mp4')
