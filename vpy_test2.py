#!/usr/bin/env python3

#Benchmark  python-mpv with vapoursynth support (pylibmpv backend)

#Version : Berlin, Take my breath away (https://www.youtube.com/watch?v=fUis9yny_lI)
#Authors:  SoSie-js  and Neinseg
#Post: https://github.com/jaseg/python-mpv/issues/172?_pjax=%23repo-content-pjax-container#issuecomment-889701254

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

#Force the use local mpv.py, else will use one installed as module with sudo pip3 install python-mpv (mpv-0.5.2 as of today) 
includepath()

import mpv
import functools
import logging
import pickle

#Ensures absolute path for the vaoursynth scriipt
script_path= includepath("tests/vpy_test2.vpy",False)

def score(loglevel, component, message):
    score='[{}] {}: {}'.format(loglevel, component, message)
    print(score)
    scores.write(score+chr(13))

#Now the fun starts

print("Top gun chaase "+script_path)
try:
    with open('log_topgun.txt', 'a+') as scores:
         scores.write("----- game starts with "+__file__+"---"+chr(13))
         player = mpv.MPV(vo='x11', log_handler=score, loglevel='debug', player_operation_mode='pseudo-gui', input_default_bindings=True, input_vo_keyboard=True) #config=True,
         #player.play("file://"+script_path) # FAILS unrecognized file format (reason 4), even if config is set
         player.loadfile(script_path, demuxer_lavf_format='vapoursynth')
         scores.write("----- loadfile is over "+chr(13))
         player.wait_for_playback()
         scores.write("----- game over ---"+chr(13))
except NameError as err:
    print("Name error: {0}".format(err))
except: # catch *all* exceptions
    e = sys.exc_info()[0]
    logging.error( "<p>Player Error: %s</p>" % e )
