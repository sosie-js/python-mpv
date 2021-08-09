#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mpv
import subprocess
import shutil

"""python vspipe to mpv helper."""
    
def pyvspipempv(script_path): #Works but unidirectional stream

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