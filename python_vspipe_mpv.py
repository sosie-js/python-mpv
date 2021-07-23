#import mpv
#player = mpv.MPV(ytdl=True)
#player.play('https://youtu.be/DOmdB7D-pUU')
#player = mpv.MPV()
#player.play('file://Untitled.vpy')
#player.wait_for_playback()


#!/usr/bin/env python3
import mpv
import subprocess

player = mpv.MPV()
@player.python_stream('foo')
def reader():
	with open('log.txt', 'ab+') as out:
		p = subprocess.Popen(['/usr/bin/vspipe version.vpy -  --y4m' ], shell=True, stdout=subprocess.PIPE)
		std_out, std_error = p.communicate()
	# Write to the file
	if std_error:
		out.write( std_error )
	yield std_out

player.play('python://foo')
player.wait_for_playback()
