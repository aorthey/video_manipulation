#!/usr/bin/python
import ffmpeg
from src.Video import Video
from PIL import Image

filename = 'logos/introscreen.png'

#[ ] Videos should end with last stone being placed
#[ ] Alignment of text is not centered
#[ ] Make it not so high resolution to get under 20MB

# video1 = Video('data/RSS/RSS_FIT.mp4')
# video2 = Video('data/RSS/RSS_tower.mp4')
# video3 = Video('data/RSS/RSS_well.mp4')
# video4 = Video('data/RSS/RSS_wall.mp4')

title = "Long-Horizon Multi-Robot Rearrangement Planning\nfor Construction Assembly"

durationScreen = 6

##### First Screen + Title Screen
video = Video('data/RSS/RSS_wall.mp4', ss=0, duration=durationScreen)
video.addText("We develop a new algorithm to \nefficiently plan assembly sequences.")
video.addTitleScreen('data/RSS/RSS_FIT.png', duration=durationScreen)
video.addText(title, tStart=0, tEnd=durationScreen)

##### Second Screen
video2 = Video('data/RSS/RSS_tower.mp4', ss=20, duration=durationScreen)
video2.addText("Our algorithm can handle large\nheterogenous robot teams...")
video.concat(video2)

##### Screen
video3 = Video('data/RSS/RSS_well.mp4', ss=20, duration=durationScreen)
video3.addText("...arbitrary object shapes...")
video.concat(video3)

##### Screen
video4 = Video('data/RSS/RSS_handover.mp4', ss=30, duration=durationScreen)
video4.addText("...handover sequences...")
video.concat(video4)

##### Screen
video4 = Video('data/RSS/RSS_FIT.mp4', ss=100, duration=durationScreen)
video4.addText("...and long time-horizons.")
video.concat(video4)

##### Screen
# video.addStillImage('data/RSS/RSS_well.png', duration=durationScreen, \
#     text="TBD: We employ a three phase approach.")

video.addStillImage('data/RSS/RSS_all.png', duration=durationScreen, \
    text="We evaluate our algorithm on four scenarios.")

tstr = "(1) Tower: 8 Agents, 15 Parts, 45 actions."
wstr = "(2) Wall: 12 Agents, 36 Parts, 108 actions."
lstr = "(3) Well: 6 Agents, 52 Parts, 156 actions."
pstr = "(4) Pavilion: 8 Agents, 113 Parts, 339 actions."

videoT1 = Video('data/RSS/RSS_tower.mp4', ss=0, duration=2*durationScreen)
videoT1.addText(tstr)
video.concat(videoT1)

videoT2 = Video('data/RSS/RSS_tower.mp4', ss=19, duration=2*durationScreen)
videoT2.addText(tstr)
video.concat(videoT2)

videoW1 = Video('data/RSS/RSS_wall.mp4', ss=0, duration=2*durationScreen)
videoW1.addText(wstr)
video.concat(videoW1)

videoW2 = Video('data/RSS/RSS_wall.mp4', ss=30, duration=2*durationScreen)
videoW2.addText(wstr)
video.concat(videoW2)

# videoL1 = Video('data/RSS/RSS_well.mp4', ss=0, duration=2*durationScreen)
# videoL1.addText(lstr)
# video.concat(videoL1)

# videoL2 = Video('data/RSS/RSS_well.mp4', ss=61, duration=2*durationScreen)
# videoL2.addText(lstr)
# video.concat(videoL2)

videoL2 = Video('data/RSS/RSS_well.mp4', ss=52, duration=4*durationScreen)
videoL2.addText(lstr)
video.concat(videoL2)

# videoP1 = Video('data/RSS/RSS_FIT.mp4', ss=0, duration=2*durationScreen)
# videoP1.addText(pstr)
# video.concat(videoP1)
# videoP2 = Video('data/RSS/RSS_FIT.mp4', ss=155, duration=2*durationScreen)
# videoP2.addText(pstr)
# video.concat(videoP2)

videoP2 = Video('data/RSS/RSS_FIT.mp4', ss=143, duration=4*durationScreen)
videoP2.addText(pstr)
video.concat(videoP2)

video.output('data/out.mp4')
