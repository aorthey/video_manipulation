import ffmpeg
from src.Logo import Logo

class Video():
  width = 0
  height = 0
  num_frames = 0
  duration = 0
  audio_stream = []
  stream = []
  def __init__(self, filename):
    probe = ffmpeg.probe(filename)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    self.width = int(video_stream['width'])
    self.height = int(video_stream['height'])
    self.num_frames = int(video_stream['nb_frames'])
    self.duration = int(float(video_stream['duration']))
    print("Input file %s [%dx%d] %d frames."%(filename, self.width, self.height, self.num_frames))
    self.stream = ffmpeg.input(filename)

  def output(self, filename):
    self.stream = ffmpeg.output(self.audio_stream, self.stream, filename, \
        **{'b:a': '320k', 'c:a': 'libmp3lame'})

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
      # input_audio = ffmpeg.filter_(input_audio, \
      #     'afade', t='out', st=duration-fade_out, d=duration)
    # input_audio = input_audio.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)

    # self.stream = ffmpeg.concat(self.stream, input_audio, v=1, a=1)

  def addTitleScreen(self, filename, duration):
    input_still = ffmpeg.input(filename)
    input_still = ffmpeg.filter(input_still, 'scale', self.width, self.height)
    tmp_stream = self.stream.trim(start=0,end=duration)
    input_still = ffmpeg.filter([tmp_stream, input_still], 'overlay')

    # input_audio = ffmpeg.input("sounds/angelic-swell.wav")
    # input_audio = input_audio.filter('atrim',duration=duration)
    # input_still = ffmpeg.concat(input_still, input_audio, v=1, a=1)

    self.stream = ffmpeg.concat(input_still, self.stream)

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

