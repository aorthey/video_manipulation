Python library based upon ffmpeg-python (https://github.com/kkroening/ffmpeg-python) for easy creation and manipualtion of videos using scripting.

# Features

##### Load clip from file 
```
video = Video('data/clip.mp4')
```
##### Add text to video 
``` 
video.addText("Hello World") 
```
##### Change text position
```
video.addText("Hello World", position="BOTTOM_LEFT")
```
##### Add fixed picture for 10s
```
video.addStillImage('data/title.png', duration=10)
```
##### Add title screen in beginning for 5s
```
video.addTitleScreen('data/title.png', duration=5)
```
##### Concat two videos
```
video2 = Video('data/clip2.mp4')
video.concat(videoP2)
```
##### Add audio
```
video.addAudio("sounds/epic.mp3", duration=video.duration, fade_in=2, fade_out=10)
```
##### Add speaker text for 10s starting at 100s
```
video.addSpecialText("Thanos", tStart=100, tEnd=110)
```
##### Output video to file
```
video.output(filename)
```


# Requires ffmpeg version 4.3.2 (https://tecadmin.net/install-ffmpeg-on-linux/)

```
sudo add-apt-repository ppa:jonathonf/ffmpeg-4
sudo apt-get update
sudo apt-get install ffmpeg
sudo apt-get install texlive-full
sudo apt-get install python-pip python3-pip python3-wheel
python3 -m pip install setuptools 
python3 -m pip install ffmpeg
python3 -m pip install ffmpeg-python
```

