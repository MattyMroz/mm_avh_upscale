import subprocess


def cmd(command):
    subprocess.call(command, shell=True)


def clean():
    # usuń folder tmp_frames i out_frames
    cmd('rmdir /s /q tmp_frames')
    cmd('rmdir /s /q out_frames')

    # przywróc folder tmp_frames i out_frames
    cmd('mkdir tmp_frames')
    cmd('mkdir out_frames')


clean()
