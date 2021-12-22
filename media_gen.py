import os.path as path
import os
import time
import subprocess
import re
import config_reader


config = config_reader.get_config()
WORK_PATH = config['work_dir']
LEAD_IN = 2
LEAD_OUT = 2
DELIM = "<====>"


def timeid():
    return str(time.time()).replace('.', '')


def filename(f):
    if path.sep in f:
        return f.split(path.sep)[-1]
    else:
        return f


def ffprober(animefile):  # search for jpn audio track with ffprober
    JP_AUDIO_REGX = r'.+(\d\:\d)(?:\(jpn\))?: Audio.+'

    out = subprocess.check_output(
        'ffprobe "{}"'.format(animefile),
        stderr=subprocess.STDOUT,
        shell=True).decode('utf-8')
    jpn_audio = re.findall(JP_AUDIO_REGX, out)

    if len(jpn_audio) > 1:
        for j in jpn_audio:
            if '(jpn)' in j:
                jpn_audio = j
    else:
        jpn_audio = jpn_audio[0]
    jpn_audio = re.findall(r'\d\:\d', jpn_audio)[0]
    return jpn_audio  # the track number x:x


def gen_image(screenshottime, animefile, thumbname):
    cmd = ('ffmpeg -ss {}  -i "{}" -vframes:v 1 "{}" -hide_banner'
           ' -loglevel error')
    cmd = cmd.format(screenshottime, animefile, thumbname)
    os.system(cmd)


def gen_audio(animefile, start, end, tracknum, mp3name):
    cmd = ('ffmpeg -i "{}" -ss {} -to {} -map {} "{}" -hide_banner'
           ' -loglevel error')
    cmd = cmd.format(animefile, start, end, tracknum, mp3name)
    os.system(cmd)


def gen(lines):
    jpgmp3s = []
    for line in lines:
        if not line:
            continue
        (serifu, animefile, screenshottime,
            start, end) = line.split(DELIM)[0:5]
        if not serifu:
            continue
        print(serifu)
        start = float(start) - LEAD_IN
        start = start if start > 0 else 0
        end = end = str(float(end) + 2)

        audio_track = ffprober(animefile)
        # anime_name = filename(animefile)
        medianame = timeid()
        jpgname = medianame + '.jpg'
        mp3name = medianame + '.mp3'
        nopath_jpgname = jpgname
        nopath_mp3name = mp3name

        jpgname = path.join(WORK_PATH, jpgname)
        mp3name = path.join(WORK_PATH, mp3name)

        print('generating screenshot...')
        gen_image(screenshottime, animefile, jpgname)

        print('generating audio...')
        gen_audio(animefile, start, end, audio_track, mp3name)

        jpgmp3s.append([nopath_jpgname, nopath_mp3name])
    return jpgmp3s
