import vapoursynth as vs
from  vapoursynth import core
print(core.version())
clip=core.std.BlankClip(format=vs.YUV420P8)
clip=core.text.FrameNum(clip,7,2)
clip=core.text.Text(clip,core.version(),9,2)
msg="Add the two lines to ~/.config/mpv/config:"+chr(13)+"[extension.vpy]"+chr(13)+"demuxer-lavf-format=vapoursynth"
clip=core.text.Text(clip,"To play directly vapoursynth files,,",4,2)
clip=core.text.Text(clip,msg,1,2)
import mvsfunc as mvf
clip = mvf.ToYUV(clip,matrix = "709", css = "420", depth = 8) 
clip.set_output()	
