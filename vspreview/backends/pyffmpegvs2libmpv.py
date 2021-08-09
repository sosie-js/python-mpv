import subprocess
import shlex
import mpv
import shutil

#NOTE: ~/.config/mpv/input config should contains to seek by frame
#RIGHT frame-step   
#LEFT  frame-back-step 


def pyffmpegvs2libmpv(script_path): 
    """ Works using libmpv but halts/go, as if buffering like hell"""
    player = mpv.MPV(config=True)
    @player.python_stream('foo')
    def reader():
        with open('log.txt', 'ab+') as out:
            ffmpeg = shutil.which('ffmpeg')
            options=' -loglevel fatal -hide_banner -f vapoursynth -i '+script_path+' -nostdin -f yuv4mpegpipe -strict -1 -pix_fmt yuv420p - '
                     
            p = subprocess.Popen([ffmpeg+' '+options], shell=True, stdout=subprocess.PIPE)
            std_out, std_error = p.communicate()
            # Write to the file
            if std_error:
               out.write( std_error )
            yield std_out

    player.play('python://foo')
    player.wait_for_playback()
