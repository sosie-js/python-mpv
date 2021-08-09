#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""version_opencv.py: Opencv Vapoursynth Python sample."""

__author__ = "SoSie and WolframRhodium"
__copyright__ = "Copyright 2021, part of the python-mpv-vapoursynth-preview Project (see on github)"
__credits__ = ["WolframRhodium", "Sebastian Goette (Jaseg)", "Olivier Lutzwiller(SoSie)"]
__license__ = "GPL"
__version__ = "1.1.0"
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

#Python equivalent of package.path = package.path .. ";" ..script_dir.. rel_path
def includepath(rel_path="",register=True):
    # Import scripts folder 
    script_dir = os.path.dirname(__file__)
    dir=os.path.join(script_dir, rel_path)
    if(register):
        sys.path.append(os.path.abspath(dir))
    return dir

#This next line is required in vapoursynth, else the vspreview module will not be found
includepath()
from vspreview.backends.info import *
from vspreview.backends.opencv import opencv as opencv_vscript_loader

"""
   NOTE: We play with WolframRhodium's pencilSketch as sample and we render 
   the result with mpv backend (only fully working and stable for now) ie 
    in a unix shell "mpv --demuxer-lavf-format=vapoursynth version_opencv.vpy" to see the video result
"""

#--> Set the input video, we use Sebastian test video.
video ="tests/test.webm"

#--> set the wished target YUv video (dimension , normally should match video settings
#but here we reduced the size, todo introduce proc core) 
width=640
height=480
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
    resized_img = resize_core2(original_img, width, height)
    img=cv2.pencilSketch(resized_img)[1]
    return img

#--> Show the recipe
if(__name__ == "__main__"):
    show_python_vapoursynth_backend(video,'opencv',__version__)
    print("To view the resulting video, use mpv --demuxer-lavf-format=vapoursynth version_opencv.vpy ")

#--> Cook the cake
if(__name__ == "__vapoursynth__"):
    clip = opencv_vscript_loader(includepath(video,False), opencv_core, verbose,width=width, height=height, matrix = matrix, css = css, depth = depth )
    clip.set_output()	
