
import logging
import os
from   pathlib  import * #Path
import sys

import vapoursynth as     vs

#from vspreviewMPV.bridge import mpv


def main() -> None:
    from argparse import ArgumentParser

    logging.basicConfig(format='{asctime}: {levelname}: {message}',
                        style='{', level=logging.DEBUG)
    logging.Formatter.default_msec_format = '%s.%03d'

    check_versions()

    parser = ArgumentParser()

    parser.add_argument('backend', help='Backend to use',
                        type=Path, nargs='?')
    parser.add_argument('script_path', help='Path to Vapoursynth script',
                        type=Path, nargs='?')
    parser.add_argument('-a', '--external-args', type=str,
                        help='Arguments that will be passed to scripts')
    args = parser.parse_args()

    if args.script_path is None:
        print('Script path required.')
        sys.exit(1)

    script_path = args.script_path.absolute() #dont follow links like resolve()
    if not script_path.exists():
        print('Script path is invalid.')
        sys.exit(1)

   #convert pathlib.PosixPath to str so  script_path.encode() will work
    script_path=str(script_path)

    backend=str(args.backend)
    print("Using backend '"+backend + "' for playing '"+script_path+"'")
    
    if(backend == 'pympv'):
        # this works but does not use mpv.py (libmpv from python)
        import subprocess
        temp_file = open("temp.txt",'w')
        proc=['/usr/local/bin/mpv']
        if script_path.endswith('.vpy'):
            proc.append('--demuxer-lavf-format=vapoursynth')
        proc.append(script_path)
        subprocess.call(proc, stdout=temp_file)
        with open("temp.txt",'r') as file:
           output = file.read()
        print(output)
    elif(backend=='pylibmpv') :
        import mpv
        import functools
        import sys
        import pickle
        try:
            #config=True,
            player = mpv.MPV(vo='x11', log_handler=print, loglevel='debug', player_operation_mode='pseudo-gui')
            #player.play("file://"+script_path) # FAILS unrecognized file format (reason 4), even if config is set
            player.loadfile(script_path, demuxer_lavf_format='vapoursynth')
            player.wait_for_playback()
        except NameError as err:
            print("Name error: {0}".format(err))
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            logging.error( "<p>Player Error: %s</p>" % e )
    elif(backend=='pyvspipempv') :
        import mpv
        import subprocess

        player = mpv.MPV(config=True)
        @player.python_stream('foo')
        def reader():
	        with open('log.txt', 'ab+') as out:
		        p = subprocess.Popen(['/usr/bin/vspipe '+script_path+' -  --y4m' ], shell=True, stdout=subprocess.PIPE)
		        std_out, std_error = p.communicate()
	        # Write to the file
	        if std_error:
		        out.write( std_error )
	        yield std_out

        player.play('python://foo')
        player.wait_for_playback()
    print("Done")

"""
    
"""
  

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
