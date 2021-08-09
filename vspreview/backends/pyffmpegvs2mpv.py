import subprocess
import shlex
import mpv
import shutil

#NOTE: ~/.config/mpv/input config should contains to seek by frame
#RIGHT frame-step   
#LEFT  frame-back-step 


def pyffmpegvs2mpv(script_path):

    """Method that works chaining ffmpeg to mpv, but not using libmpv,imho  equivalent to pympv backend """

    # 1.Build the ffmpeg part
    ffmpeg = shutil.which('ffmpeg')
    options=" -loglevel fatal -hide_banner -f vapoursynth -i '"+script_path+"' -nostdin -f yuv4mpegpipe -strict -1 -pix_fmt yuv420p - "
    command= ffmpeg +' '+options
    options=shlex.split(command)

    fp = subprocess.Popen(options, stdout=subprocess.PIPE)
    #std_out, std_error = fp.communicate()

    # 2.Bridge it to mpv
    print("Running "+command+'| mpv -')
    mpv = shutil.which('mpv')
    proc=[]
    proc.append(mpv)    
    proc.append("-") 
    #print(proc)
    player = subprocess.Popen(proc, stdin=fp.stdout, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    std_out, std_error = player.communicate()
    
