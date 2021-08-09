#!/usr/bin/python3

#Benchmark python-mpv with vapoursynth/avisynth+ support with misc backends 
#Version : VapeurSauce 1.0
#Author:  SoSie-js  
 
import argparse
from argparse import ArgumentParser

import logging
import os
from   pathlib  import * #Path
import sys

import vapoursynth as     vs

version='VapeurSauce 1.0'

def install_custom_log():
    logging.basicConfig(format='{asctime}: {levelname}: {message}',
                        style='{', level=logging.DEBUG)
    logging.Formatter.default_msec_format = '%s.%03d'


def create_parser():

    parser = ArgumentParser(
        description="Specify the backend and the vapoursynth with script_path to use"
    )

    parser.add_argument('backend', help='Backend to use',
                        type=Path, nargs='?', default ='pylibmpv')
    parser.add_argument('script_path', help='Path to Vapoursynth script',
                        type=Path, nargs='?')
    parser.add_argument('-a', '--external-args', type=str,
                        help='Arguments that will be passed to scripts')
  
    return parser

from vspreview.backends.info import *

def main():
    
    install_custom_log()

    check_versions()

    args = create_parser().parse_args()

    if args.script_path is None:
        print('python-mpv-vapoursynth-preview ('+version+' version) requires arguments, -h for help')
        sys.exit(1)

    script_path = args.script_path.absolute() #dont follow links like resolve()
    if not script_path.exists():
        print('Script path is invalid.')
        sys.exit(1)


    #convert pathlib.PosixPath to str so  script_path.encode() will work
    script_path=str(script_path)

    backend=str(args.backend)
    print(version+" use backend '"+backend + "' for playing '"+script_path+"'")
    
    if(backend == 'pympv'): # -> Works "<->" using -demuxer-lavf-format=vapoursynth of mpv
        
        from vspreview.backends.pympv import pympv
        pympv(script_path)

    elif(backend == 'pyffmpegvs2mpv'): # Works "<->" using ffmpeg vapoursynth format through lav

       from vspreview.backends.pyffmpegvs2mpv import pyffmpegvs2mpv
       pyffmpegvs2mpv(script_path) 

    elif(backend == 'pyffmpegvs2libmpv'): # Works "->" ,  using mpv.py (libmpv from python) but buffers like hell é_è

       from vspreview.backends.pyffmpegvs2libmpv import pyffmpegvs2libmpv
       pyffmpegvs2libmpv(script_path) 

    elif(backend=='pylibmpv') : # -> Sucks, instable play crazingly ,please use the py version to debug instead (Need help to fix!)
    
       from vspreview.backends.pylibmpv import pylibmpv
       pylibmpv(script_path) 
    
    elif(backend=='pyrawpipempv') : #--> Sucks, black screen directly on mpv, terminal locked
        
        from vspreview.backends.pyrawpipempv import pyrawpipempv
        pyrawpipempv(script_path)

    elif(backend=='pyvspipempv') : # -> Works, "->" , ie not go back in the stream, slower people said, buffering as well
        from vspreview.backends.pyvspipempv import pyvspipempv
        pyvspipempv(script_path)
        
    elif(backend=='pyavs2yuvmpv') : # Works "->" but no sound support is intended for future
        
        from vspreview.backends.pyavs2yuvmpv import pyavs2yuvmpv
        pyavs2yuvmpv(script_path)
   
    else:
        print("Unsupported backend")


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

if __name__ == '__main__':
    main()
