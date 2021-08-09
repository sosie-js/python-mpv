#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""version_opencv.py: Opencv Vapoursynth Python sample."""

__author__ = "SoSie and WolframRhodium"
__copyright__ = "Copyright 2021, part of the python-mpv-vapoursynth-preview Project (see on github)"
__credits__ = ["WolframRhodium", "Sebastian Goette (Jaseg)", "Olivier Lutzwiller(SoSie)"]
__license__ = "GPL"
__version__ = "1.1.1"
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

from vspreview.backends.info import *

#Python equivalent of package.path = package.path .. ";" ..script_dir.. rel_path
"""def includepath(rel_path="",register=True):
    # Import scripts folder 
    script_dir = os.path.dirname(__file__)
    dir=os.path.join(script_dir, rel_path)
    if(register):
        sys.path.append(os.path.abspath(dir))
    return dir"""

#Now, an absolute path should be given for video should be given 
def opencv(video,cv_script_handler_core, show_backend, **kwargs):

    #default Yuv params values
    params={
         "matrix" : "709",
         "css" : "420", 
         "depth" : 8
    }
    
    #Override default values if provided
    for name, value in zip(kwargs, kwargs.values()):
            params[name] = value

    # 0. show what we do 
    show_python_vapoursynth_backend(video,'opencv',__version__, str(params["width"])+ "x"+str(params["height"])+ " in yuv"+str(params["css"])+"P"+str(params["depth"])+"(BT"+str(params["matrix"])+")")

    #1. ensure the clip is in RGB format.
    #abs_file_path= includepath(video, False)
    rgb = mvf.ToRGB(core.ffms2.Source(source= video))

    #2. since the size of the output is not equal to the input. If the cv2.resize is removed, this change is not necessar
    empty = core.std.BlankClip(rgb, width=params["width"], height=params["height"])
    clip = mufnp.numpy_process([empty,rgb], cv_script_handler_core, input_per_plane=False, output_per_plane=False)
    
    #3. set the target YUv video
    clip = mvf.ToYUV(clip,params["matrix"], params["css"], params["depth"]) 
    return clip
