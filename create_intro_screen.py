from PIL import Image

img = Image.new('RGB', (300, 200), (207, 236, 207))
img.save("logos/introscreen.png")

import ffmpeg
input_still = ffmpeg.input("logos/introscreen.png", pattern_type='glob', t=8, framerate=24)
input_audio = ffmpeg.input("sounds/angelic-swell.wav")

input_still = ffmpeg.concat(input_still, input_audio, v=1, a=1)
input_still = ffmpeg.output(input_still, "output.mp4")
ffmpeg.run(input_still, overwrite_output=True)
