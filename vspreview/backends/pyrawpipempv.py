#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import mpv
import functools
import pickle
from pprint import pprint

import json

def _get_current_environment(init_env=''):
    
    import os
    import shlex
    import subprocess

    #https://qastack.fr/programming/3503719/emulating-bash-source-in-python
    if(init_env):
        command = shlex.split("env -i bash -c 'source "+init_env+" && env'")

        proc = subprocess.Popen(command, stdout = subprocess.PIPE)

        #https://stackoverflow.com/questions/33054527/typeerror-a-bytes-like-object-is-required-not-str-when-writing-to-a-file-in
        lines = [x.decode('utf8').strip() for x in proc.stdout.readlines()]

        #for line in proc.stdout:
        for line in lines:
          (key, _, value) = line.partition("=")
          os.environ[key] = value
        proc.communicate()
        #pprint(dict(os.environ))

    env=dict(os.environ)
    return env

"""python raw vs code pipe to mpv helper."""

def pyrawpipempv(script_path):
 
    env=None
    #import web_pdb; web_pdb.set_trace() 
    try:
      env = get_current_environment()
    except Exception:
      try:	
        env = vpy_current_environment()
      except Exception:
        env=_get_current_environment()
        
    print(json.dumps(env))


    def score(loglevel, component, message):
        score='[{}] {}: {}'.format(loglevel, component, message)
        print(score)
        scores.write(score+chr(13))
    
    with open('log_topgun.txt', 'a+') as scores:
        player = mpv.MPV(vo='x11', log_handler=score, loglevel='debug', player_operation_mode='pseudo-gui', input_default_bindings=True, input_vo_keyboard=True)
                #scripts='debug.lua', script_opts='debug-scriptpath='+script_path)
        @player.python_stream('vps-test')
        def reader():

            with open(script_path, 'r') as out:
                rawvpy=out.read().encode()
            with open('vsrawscript.txt', 'ab') as out:
                out.write(rawvpy)
            yield rawvpy 

        player.loadfile('python://vps-test', demuxer_lavf_format='vapoursynth')
        player.wait_for_playback()
        print("Done")