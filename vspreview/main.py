
import logging
import os
from   pathlib  import * #Path
import sys

import vapoursynth as     vs
import mpv
#from vspreviewMPV.bridge import mpv


def main() -> None:
    from argparse import ArgumentParser

    logging.basicConfig(format='{asctime}: {levelname}: {message}',
                        style='{', level=logging.DEBUG)
    logging.Formatter.default_msec_format = '%s.%03d'

    check_versions()

    parser = ArgumentParser()
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

    #Se to False if you dare to debug the issue (Any help is welcomed)    
    failsafe= True

    if(failsafe):
        # this works but does not use mpv.py (libmpv from python)
        import subprocess
        temp_file = open("temp.txt",'w')
        subprocess.call(['/usr/local/bin/mpv', script_path], stdout=temp_file)
        with open("temp.txt",'r') as file:
           output = file.read()
        print(output)
    else:
        # this should work, but nothing happen !
        try:
            player = mpv.MPV(config=True)
            player.play("file:/"+script_path)
            player.wait_for_playback()
        except NameError as err:
            print("Name error: {0}".format(err))
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            logging.error( "<p>Player Error: %s</p>" % e )
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
