import ffmpeg
from src.Logo import Logo

class Video():
  width = 0
  height = 0
  num_frames = 0
  def __init__(self, filename):
    probe = ffmpeg.probe(filename)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    self.width = int(video_stream['width'])
    self.height = int(video_stream['height'])
    self.num_frames = int(video_stream['nb_frames'])
    print("Input file %s [%dx%d] %d frames."%(filename, self.width, self.height, self.num_frames))
    self.stream = ffmpeg.input(filename)

  def output(self, filename):
    self.stream = ffmpeg.output(self.stream, filename)
    ffmpeg.run(self.stream, overwrite_output=True)

  def addLogo(self, filename, position, scale):
    logo = Logo(filename)
    logo.setTotalWidthHeight(self.width, self.height)
    logo.scale(scale)
    [x,y] = logo.getPosition(position)
    self.stream = ffmpeg.filter([self.stream, logo.asStream()], 'overlay', x, y)
