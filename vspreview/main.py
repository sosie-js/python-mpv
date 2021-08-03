#!/usr/bin/python3

#Benchmark python-mpv with vapoursynth support with misc backends 
#Version : JJGoldman, Je marche seul  (https://www.youtube.com/watch?v=5AS0wPLnAhY)
#Author:  SoSie-js  
 
import argparse
from argparse import ArgumentParser

import logging
import os
from   pathlib  import * #Path
import sys

import vapoursynth as     vs

version='JJGoldman'

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
    
    if(backend == 'pympv'): # -> Works

        # this works but does not use mpv.py (libmpv from python)
        import subprocess
        temp_file = open("temp.txt",'w')
        import shutil
        mpv = shutil.which('mpv') #'/usr/local/bin/mpv'
        proc=[]
        proc.append('mpv')
        if script_path.endswith('.vpy'):
            proc.append('--demuxer-lavf-format=vapoursynth')
        proc.append(script_path)
        subprocess.call(proc, stdout=temp_file)
        temp_file.close()
        with open("temp.txt",'r') as file:
           output = file.read()
        print(output)

    elif(backend == 'pyffmpegvs2mpv'): # -> How to run this?, i tried different ways but no success to repoduce the bash command that works...é_è

        import subprocess
        import shlex
        import mpv
        import shutil

        ffmpeg = shutil.which('ffmpeg')
        ffmpegvs=ffmpeg+' -loglevel fatal -hide_banner -f vapoursynth -i '+script_path+' -nostdin -f yuv4mpegpipe -strict -1 -pix_fmt yuv420p - '
        temp_file = open("temp.txt",'w')
        command= ffmpegvs +'| mpv -'  
        print("Running "+command)
        proc=shlex.split(command)
        subprocess.call(proc,  shell=True, stdout=temp_file)
        temp_file.close()
        temp_file = open("temp.txt",'r')
        print(temp_file.read())
        temp_file.close()
        """player = mpv.MPV(config=True)
        @player.python_stream('foo')
        def reader():
            with open('log.txt', 'ab+') as out:
                
                proc = shlex.split(command)
                
                #command= ffmpegvs+'| mpv -'
                #print("Running "+command)
                '''proc=['ffmpeg']
                proc.append('-loglevel')
                proc.append('fatal')
                proc.append('-hide_banner')
                proc.append('-f')
                proc.append('vapoursynth')
                proc.append('-i')
                proc.append(script_path)
                proc.append('-nostdin')
                proc.append('-f')
                proc.append('yuv4mpegpipe')
                proc.append('-strict')
                proc.append('-1')
                proc.append('-pix_fmt')
                proc.append('yuv420p')
                proc.append('-')
                print(proc)
                proc=['/usr/bin/ffmpeg', '-loglevel', 'fatal', '-hide_banner', '-f', 'vapoursynth', '-i', 'version.vpy', '-nostdin', '-f', 'yuv4mpegpipe', '-strict', '-1', '-pix_fmt', 'yuv420p', '-']
                '''
                p = subprocess.Popen(proc, shell=True, stdout=subprocess.PIPE)
                std_out, std_error = p.communicate()
                # Write to the file
                if std_error:
                   out.write( std_error )
                   print(std_error)
                yield std_out

        player.play('python://foo')
        player.wait_for_playback()"""
    elif(backend=='pylibmpv') : # -> Sucks
        import mpv
        import functools
        import pickle
        
        def score(loglevel, component, message):
            score='[{}] {}: {}'.format(loglevel, component, message)
            print(score)
            scores.write(score+chr(13))

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
    elif(backend=='pyrawpipempv') : #--> sucks

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
    elif(backend=='pyvspipempv') : # -> Works, but can not go back in the stream, slower people said
        import mpv
        import subprocess
        import shutil
        vspipe = shutil.which('vspipe')

        player = mpv.MPV(config=True)
        @player.python_stream('foo')
        def reader():
            with open('log.txt', 'ab+') as out:
                p = subprocess.Popen([vspipe+' '+script_path+' -  --y4m' ], shell=True, stdout=subprocess.PIPE)
                std_out, std_error = p.communicate()
                # Write to the file
                if std_error:
                   out.write( std_error )
                yield std_out

        player.play('python://foo')
        player.wait_for_playback()
        print("Done")
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