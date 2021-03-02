import ffmpeg
from ffmpeg.nodes import InputNode
import sys
import numpy as np
from src.Logo import Logo
from random import randrange

class Video():
  width = 0
  height = 0
  num_frames = 0
  duration = 0
  audio_stream = None
  framerate = 0
  stream = None

  def __init__(self, filename=None, ss=0, duration=-1):
    if filename is not None:
      probe = ffmpeg.probe(filename)
      video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
      self.width = int(video_stream['width'])
      self.height = int(video_stream['height'])
      self.num_frames = int(video_stream['nb_frames'])
      self.duration = int(float(video_stream['duration']))
      avg_frame_rate = video_stream['avg_frame_rate']
      n = np.array(avg_frame_rate.split('/'), dtype='float')
      self.framerate = int(float(n[0]/n[1]))
      print("Input file %s [%dx%d] %d frames and framerate %d."%(filename, \
          self.width, self.height, self.num_frames, self.framerate))
      if duration > 0:
        self.stream = ffmpeg.input(filename,ss=ss,t=duration)
        self.duration = duration
      else:
        self.stream = ffmpeg.input(filename,ss=ss)

  def output(self, filename):
    if self.audio_stream is not None:
      self.stream = ffmpeg.output(self.audio_stream, self.stream, filename, \
          **{'b:a': '320k', 'c:a': 'libmp3lame'})
    else:
      self.stream = ffmpeg.output(self.stream, filename, crf='30')

    ffmpeg.run(self.stream, overwrite_output=True)

  def repeatLastFrame(self, duration):
    self.stream = ffmpeg.filter_(self.stream, 'tpad',\
        stop_mode='clone', stop_duration=duration)

  def addAudio(self, filename, duration=-1, fade_out=-1, fade_in=-1):
    self.audio_stream = ffmpeg.input(filename)
    if duration > 0:
      self.audio_stream = ffmpeg.filter(self.audio_stream, 'atrim',\
          start=0, duration=duration)
    if fade_out > 0:
      self.audio_stream = ffmpeg.filter(self.audio_stream, 'afade', type='out', \
          start_time = duration-fade_out, duration=fade_out)
    if fade_in > 0:
      self.audio_stream = ffmpeg.filter(self.audio_stream, 'afade', type='in', \
          start_time = 0, duration=fade_in)

  def addTitleScreen(self, filename, duration):
    input_still = ffmpeg.input(filename, r=self.framerate)
    input_still = ffmpeg.filter(input_still, 'scale', self.width, self.height)

    input_still = ffmpeg.filter_(input_still, 'tpad',\
        stop_mode='clone', stop_duration=duration)

    self.stream = ffmpeg.concat(input_still, self.stream)
    self.duration += duration

  def addStillImage(self, filename, duration, text=None):
    # kwargs = ['filename=%s'%filename, 'r=%d'%self.framerate]
    # # kwargs['filename'] = filename
    # # kwargs['r'] = self.framerate
    # ctr = randrange(1000)
    # input_still = InputNode(filename, kwargs=kwargs).stream(filename+str(ctr))

    input_still = ffmpeg.input(filename, r=self.framerate)
    # input_still = ffmpeg.filter(input_still, 'setsar', 1)
    input_still = ffmpeg.filter(input_still, 'scale', self.width, self.height)
    input_still = ffmpeg.filter_(input_still, 'tpad',\
        stop_mode='clone', stop_duration=duration)



    self.stream = ffmpeg.concat(self.stream, input_still)
    self.duration += duration

    if text is not None:
      self.addText(text, tStart=self.duration-duration)

  def concat(self, video):
    video.stream = ffmpeg.filter(video.stream, 'scale', self.width, self.height)
    # print(video.num_frames, self.num_frames)
    # sys.exit(0)
    self.stream = ffmpeg.concat(self.stream, video.stream)
    self.duration += video.duration

  def addText(self, text, x=0, y=0, tStart=0, tEnd=-1):
    if tEnd < 0:
      tEnd = self.duration

    lines = text.split('\n')

    for lc, line in enumerate(lines):
      # print(lc,line)
      yoffset = (len(lines)-lc)
    # [in]drawtext=font='Arial': text='This is text line
    # 1':x=(w-tw)/2:y=((h-text_h)/2)-(text_h-(th/4)): fontsize=55:
    #   fontcolor=red, drawtext=font='Arial': text='This is text line
    #   2':x=(w-tw)/2:y=((h-text_h)/2)+(text_h-(th/4)): fontsize=55:
    #     fontcolor=green[out]


      padding=0.05*self.height
      padding_w=0.05*self.width

      fonttype = "/usr/share/fonts/truetype/cmr10.ttf"
      self.stream = ffmpeg.filter_(self.stream, 'drawtext', \
          fontfile=fonttype, text=line, fontcolor='white',\
          x="%f-text_w/2"%(0.5*self.width), \
          y="%f-%d*(text_h+%f)"%(self.height, yoffset, padding), \
          enable='between(t,%d,%d)'%(tStart, tEnd),\
          fontsize=80, box=1, boxcolor="#AFAFAF", boxborderw=0.5*padding)

        # os.system("""ffmpeg -i merola.mp4 -vf
        #     drawtext="fontfile=/path/to/font.ttf: \
        #             text={text}: fontcolor=white: fontsize=24: box=1:
        #             boxcolor=black@0.5: \
        #                     boxborderw=5: x=0: y=h-30" -codec:a copy
        #                     output.mp4""")




  def addLogos(self, filenames, scale, duration = -1):
    logos = []
    lw = 0
    for f in filenames:
      logo = Logo(f)
      logo.setTotalWidthHeight(self.width, self.height)
      logo.scale(scale)
      logos.append(logo)
      lw += logo.width

    xspacing = self.width - lw
    N = len(logos)-1
    padding = 10
    dx = (xspacing-2*padding)/N

    print("width:",self.width,"logos width:",lw,"dx:",dx)

    xoffset = padding
    for logo in logos:
      [x,y] = logo.getPosition("BOTTOM_LEFT")
      x = xoffset
      if duration > 0:
        self.stream = ffmpeg.filter_([self.stream, logo.asStream()], \
            'overlay', x=x, y=y, enable='between(t,0,%d)'%duration)
      else:
        self.stream = ffmpeg.filter([self.stream, logo.asStream()], \
            'overlay', x, y)
      xoffset = xoffset + logo.width + dx



  def addLogo(self, filename, position, scale, duration = -1):
    logo = Logo(filename)
    logo.setTotalWidthHeight(self.width, self.height)
    logo.scale(scale)
    [x,y] = logo.getPosition(position)

    if duration > 0:
      self.stream = ffmpeg.filter_([self.stream, logo.asStream()], \
          'overlay', x=x, y=y, enable='between(t,0,%d)'%duration)
    else:
      self.stream = ffmpeg.filter([self.stream, logo.asStream()], \
          'overlay', x, y)
    # self.stream = ffmpeg.overlay(self.stream, logo.asStream(), x=x, y=y, eof_action='pass')

