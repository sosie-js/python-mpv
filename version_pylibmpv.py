#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import os
from   pathlib  import * #Path
import sys

import mpv
import functools
import pickle

"""
  This backend has a memory flaw, it seems to render everything rescursively on call
  "./version_pylibmpv.py  version.vpy" except the wished version.vpy to end on a black screen on mpv!
 . it a long non ending story  with jaseg and neinseg the author of python-mpv,
  see by yourself,   https://github.com/jaseg/python-mpv/issues/172
  I dunno if it is a python3 or a cpython related issue, or mpv.  If you find how to fix it 
  tell me, call the bunny, he will be very happy. Thanks. SoSie
"""

import argparse
from argparse import ArgumentParser


import vapoursynth as     vs

version='VapeurSauce'
backend='pylibmpv'
script_path=''
folder = Path(__file__).parent
script_path=str(folder.joinpath(script_path))

def install_custom_log():
    logging.basicConfig(format='{asctime}: {levelname}: {message}',
                        style='{', level=logging.DEBUG)
    logging.Formatter.default_msec_format = '%s.%03d'


def create_parser():

    parser = ArgumentParser(
        description="Specify the vapoursynth with script_path to use"
    )

    parser.add_argument('script_path', help='Path to Vapoursynth script',
                        type=Path, nargs='?')
   
    return parser


def main():
    
    install_custom_log()

    check_versions()

    args = create_parser().parse_args()

    if args.script_path is None:
        print('python-mpv-vapoursynth-preview ('+version+' version) require argument, -h for help')
        sys.exit(1)

    script_path = args.script_path.absolute() #dont follow links like resolve()
    if not script_path.exists():
        print('Script path is invalid.')
        sys.exit(1)


    #convert pathlib.PosixPath to str so  script_path.encode() will work
    script_path=str(script_path)

    print(version+" use backend '"+backend + "' for playing '"+script_path+"'")
    

def check_versions() -> bool:
    from pkg_resources import get_distribution
    from platform import python_version

    failed = False

    if sys.version_info < (3, 9, 0, 'final', 0):
        logging.warning('VSPreview is not tested on Python versions prior to 3.9, but you have {} {}. Use at your own risk.'
                        .format(python_version(), sys.version_info.releaselevel))
        failed = True

    #if get_distribution('PyQt5').version < '5.15':
     #   logging.warning('VSPreview is not tested on PyQt5 versions prior to 5.15, but you have {}. Use at your own risk.'
     #                   .format(get_distribution('PyQt5').version))
     #   failed = True

    if vs.core.version_number() < 53:
        logging.warning('VSPreview is not tested on VapourSynth versions prior to 53, but you have {}. Use at your own risk.'
                        .format(vs.core.version_number()))
        failed = True

    return not failed



def score(loglevel, component, message):
    score='[{}] {}: {}'.format(loglevel, component, message)
    print(score)
    scores.write(score+chr(13))


main()

try:
    with open('log_topgun.txt', 'a+') as scores:
        scores.write("----- game starts with "+__file__+"---"+chr(13))
        player = mpv.MPV(vo='x11', log_handler=print, loglevel='debug', player_operation_mode='pseudo-gui', input_default_bindings=True, input_vo_keyboard=True)
        #scripts='debug.lua', script_opts='debug-scriptpath='+script_path) #config=True,
        #player.play("file://"+script_path) # FAILS unrecognized file format (reason 4), even if config is s
        player.loadfile(script_path, demuxer_lavf_format='vapoursynth')
        player.wait_for_playback()
        scores.write("----- game over ---"+chr(13))
except NameError as err:
    print("Name error: {0}".format(err))
except: # catch *all* exceptions
    e = sys.exc_info()[0]
    logging.error( "<p>Player Error: %s</p>" % e )