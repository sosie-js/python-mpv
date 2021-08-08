#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""version_opencv.py: Opencv Vapoursynth Python sample."""

__author__ = "SoSie and WolframRhodium"
__copyright__ = "Copyright 2021, part of the python-mpv-vapoursynth-preview Project (see on github)"
__credits__ = ["WolframRhodium", "Sebastian Goette (Jaseg)", "Olivier Lutzwiller(SoSie)"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "SoSie"
__email__ = "sosie@sos-productions.com"
__status__ = "Production"

import numpy as np
import cv2
import muvsfunc_numpy as mufnp

import vapoursynth as vs
from  vapoursynth import core

import mvsfunc as mvf

import os
import sys

"""
   NOTE: We play with WolframRhodium's pencilSketch as sample and we render 
   the result with mpv backend (only fully working and stable for now) ie 
    in a unix shell "mpv --demuxer-lavf-format=vapoursynth version_opencv.vpy" to see the video result
"""

#--> Set the input video, we use Sebastian test video.
video ="tests/test.webm"

#--> set the wished target YUv video (dimension , normally should match video settings
#but here we reduced the size, todo introduce proc core) 
w=640
h=480
matrix = "709"
css = "420"
depth = 8

#--> decide whether or not to put a cherry on the cake
verbose= True

#---> Now your opencv user script baby to transform your video into a cartoon!
def resize_core2(img, w, h):
    return cv2.resize(img, dsize=(w, h), interpolation=cv2.INTER_CUBIC)

def opencv_core(empty, original_img):
    # resize image
    resized_img = resize_core2(original_img, w, h)
    img=cv2.pencilSketch(resized_img)[1]
    return img

"""===== DON'TEDIT OR EVEN CROSS THIS LINE DUDE, THIS IS DANGEROUS! ====="""

def show_python_vapoursynth_backend(video,rendering=""):
    print("========================================")
    print("Running backend pyopencv "+__version__+" on '"+video+"'")
    print("By: WolframRhodium and SoSie (08.2021)") 
    if(rendering):
        print("Rendering output settings: "+rendering)
    print("Using:")
    print(vs.__version__)
    print("Numpy "+np.__version__)
    print("OpenCv "+cv2.__version__)
    if(rendering):
        #See https://github.com/HomeOfVapourSynthEvolution/mvsfunc/blob/master/mvsfunc.py
        print("with : ToYUV function (belong to mawen1250's VapourSynth script)")
    print("========================================")

#Python equivalent of package.path = package.path .. ";" ..script_dir.. rel_path
def includepath(rel_path="",register=True):
    # Import scripts folder 
    script_dir = os.path.dirname(__file__)
    dir=os.path.join(script_dir, rel_path)
    if(register):
        sys.path.append(os.path.abspath(dir))
    return dir

def opencv_vscript_loader(video,cv_script_handler_core, show_backend, **kwargs):

    #default Yuv params values
    params={
         matrix : "709",
         css : "420", 
         depth : 8
    }
    #Override default values if provided
    for name, value in zip(kwargs, kwargs.values()):
            params[name] = value

    abs_file_path= includepath(video, False)
    
    # 0. show what we do 
    show_python_vapoursynth_backend(abs_file_path, str(w)+ "x"+str(h)+ " in yuv"+str(css)+"P"+str(depth)+"(BT"+str(matrix)+")")

    #1. ensure the clip is in RGB format.
    rgb = mvf.ToRGB(core.ffms2.Source(source= abs_file_path))

    #2. since the size of the output is not equal to the input. If the cv2.resize is removed, this change is not necessar
    empty = core.std.BlankClip(rgb, width=w, height=h)
    clip = mufnp.numpy_process([empty,rgb], cv_script_handler_core, input_per_plane=False, output_per_plane=False)
    
    #3. set the target YUv video
    clip = mvf.ToYUV(clip,params["matrix"], params["css"], params["depth"]) 
    return clip

#Cook the cake
if(__name__ == "__main__"):
    show_python_vapoursynth_backend(video)
    print("To view the resulting video, use mpv --demuxer-lavf-format=vapoursynth version_opencv.vpy ")

if(__name__ == "__vapoursynth__"):
    clip = opencv_vscript_loader(video, opencv_core, verbose,matrix = matrix, css = css, depth = depth )
    clip.set_output()	
