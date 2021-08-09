#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mpv
import subprocess
import shutil

"""python avisynth+ helper.
Requires Avs2YUV >= 0.30, see https://github.com/DJATOM/avs2yuv/issues/3"""

def pyavs2yuvmpv(script_path):
 
    
    avs2yuv = shutil.which('avs2yuv')
    player = mpv.MPV()
    @player.python_stream('foo')
    def reader():
         with open('log.txt', 'ab+') as out:
            p = subprocess.Popen([avs2yuv+' '+script_path+' -' ], shell=True, stdout=subprocess.PIPE)  
            std_out, std_error = p.communicate()
            # Write to the file
            if std_error:
               out.write( std_error )
            yield std_out
    player.play('python://foo')
    #--demuxer=rawvideo --demuxer-rawvideo-w=320 --demuxer-rawvideo-h=240 --demuxer-rawvideo-fps=29.970 --demuxer-rawvideo-mp-format=rgb32
    player.wait_for_playback()
