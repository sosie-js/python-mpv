#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""python libMpv helper."""

import mpv
import functools
import pickle

def score(loglevel, component, message):
    global scores
    score='[{}] {}: {}'.format(loglevel, component, message)
    print(score)
    scores.write(score+chr(13))

def pylibmpv(script_path):
    global scores
    try:
        with open('log_topgun.txt', 'a+') as scores:
            scores.write("----- game starts with "+__file__+"---"+chr(13))
            player = mpv.MPV(vo='x11', log_handler=score, loglevel='debug', player_operation_mode='pseudo-gui', input_default_bindings=True, input_vo_keyboard=True)
            #scripts='debug.lua', script_opts='debug-scriptpath='+script_path) #config=True,
            #player.play("file://"+script_path) # FAILS unrecognized file format (reason 4), even if config is s
            player.loadfile(script_path, demuxer_lavf_format='vapoursynth')
            #player.wait_for_playback()
            scores.write("----- game over ---"+chr(13))
    except NameError as err:
        print("Name error: {0}".format(err))
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        logging.error( "<p>Player Error: %s</p>" % e )
