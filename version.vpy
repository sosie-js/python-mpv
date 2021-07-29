
import vapoursynth as vs
from  vapoursynth import core

import jsonplus as json

#Python equivalent of package.path = package.path .. ";" ..script_dir.. rel_path
def includepath(rel_path=""):
		import os
		# Import scripts folder 
		script_dir = os.path.dirname(__file__)
		dir=os.path.join(script_dir, rel_path)
		import sys
		sys.path.append(os.path.abspath(dir))
		
includepath()
from pprint import pprint
import outputwindow		
#print(core.version())
width=800
height=600
clip=core.std.BlankClip(width=width,height=height,format=vs.YUV420P8)

clip=core.text.FrameNum(clip,7,2)


		
clip=core.text.Text(clip,core.version(),9,2)
msg="Add the two lines to ~/.config/mpv/config:"+chr(13)+"[extension.vpy]"+chr(13)+"demuxer-lavf-format=vapoursynth"
format=clip[0].format
clip_infos = {   
	'Width': clip.width,
	'Height': clip.height,
	'Frames': clip. num_frames,
	'FPS': clip.fps,
	'Format Name': format.name, #'YUV420P8'
	'Color Family': format.color_family, #'YUV'
	'Alpha': 'No',
	'Sample Type': format.sample_type , #'Integer',
	'Bits': format.bits_per_sample,
	'SubSampling W': format.subsampling_w,
	'SubSampling H': format.subsampling_h,
	'Planes':  format.num_planes
}
clip=core.text.Text(clip, "Frame informations:"+chr(13)+chr(13)+"Video:"+chr(13)+str(clip.width)+"x"+str(clip.height),4,2)
clip=core.text.Text(clip, json.dumps(clip_infos, indent=4),5,1)
clip=core.text.Text(clip,"To play directly vapoursynth files,"+msg,1,2)
try:
  env = get_current_environment()
  with env.use():
    # Do stuff inside this env.
    #pprint(env)
    dummy=0
    #import web_pdb; web_pdb.set_trace()
except Exception:
  try:	
    env = vpy_current_environment()
    with env.use():
      # Do stuff inside this env.
      #pprint(env)
      dummy=0
      #import web_pdb; web_pdb.set_trace()
  except Exception:
    env = globals()
    #pprint(env)
    dummy=0
    #import web_pdb; web_pdb.set_trace()  
import mvsfunc as mvf
clip = mvf.ToYUV(clip,matrix = "709", css = "420", depth = 8) 
#http://www.vapoursynth.com/doc/pythonreference.html#slicing-and-other-syntactic-sugar
#hide video trick, reduce to the min in time, shortcut for clip = clip.std.Trim(first=1, last=2)
#clip = clip[1:2]
#clip = core.resize.Bicubic(clip, width=10,height=10)
clip.set_output()	
