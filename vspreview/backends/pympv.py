#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""python Mpv helper."""

def pympv(script_path):
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