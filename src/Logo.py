import ffmpeg
import sys

class Logo():
  total_width = 0
  total_height = 0

  padding_percentage = 0.01 ##percentage of total_height
  width = 0
  height = 0
  scale = 1
  stream = []
  def __init__(self, filename):
    probe = ffmpeg.probe(filename)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    self.width = int(video_stream['width'])
    self.height = int(video_stream['height'])
    self.stream = ffmpeg.input(filename)

  def asStream(self):
    return self.stream

  def setTotalWidthHeight(self, width, height):
    self.total_width = width
    self.total_height = height

  def scale(self, scale):
    self.scale = scale
    desired_height = self.scale*self.total_height
    desired_width = (desired_height/self.height)*self.width
    self.stream = ffmpeg.filter(self.stream, 'scale', desired_width, desired_height)
    self.width = desired_width
    self.height = desired_height

  def getPosition(self, position):
    self.padding = self.padding_percentage*self.total_height
    if position is "BOTTOM_LEFT":
      x = self.padding
      y = self.total_height-self.height-self.padding
    elif position is "BOTTOM_RIGHT":
      x = self.total_width-self.width-self.padding
      y = self.total_height-self.height-self.padding
    elif position is "BOTTOM_MIDDLE":
      x = 0.5*self.total_width-0.5*self.width
      y = self.total_height-self.height-self.padding
    elif position is "BOTTOM_RIGHT_MIDDLE":
      x = 0.66*self.total_width
      y = self.total_height-self.height-self.padding
    elif position is "BOTTOM_LEFT_MIDDLE":
      x = 0.33*self.total_width
      y = self.total_height-self.height-self.padding
    elif position is "TOP_RIGHT":
      x = self.total_width-self.width-self.padding
      y = self.padding
    elif position is "TOP_LEFT":
      x = self.padding
      y = self.padding
    elif position is "TOP_MIDDLE":
      x = 0.5*self.total_width-0.5*self.width
      y = self.padding
    else:
      print(position,"is not known.")
      sys.exit(0)
    return [x,y]

# desired_height = 0.2*height
# desired_width = (desired_height/height_logo)*width_logo


