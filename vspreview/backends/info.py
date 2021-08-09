#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""version_opencv.py: Opencv Vapoursynth Python sample."""

__author__ = "SoSie"
__copyright__ = "Copyright 2021, part of the VapeurSauce-preview Project (see on github)"
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

def show_python_vapoursynth_backend(video,backend,version,rendering=""):
    print("=========Welcome on VapeurSauce(vSoS) preview ==============")
    print("Running backend '"+backend+"' "+version+" on '"+video+"'")
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
    print("======================================================")
