import re
import sys
import media_gen
import config_reader
from os import path as path

"""
    this file takes your Clippings.txt file
    from your kindle or the lines you saved
    using the mpv script and makes a csv file
    | line | [  ] | {}
    the walkthrough script will ask you to
    fill in the word(s) you want definitions
    for in the square brackets.
"""


config = config_reader.get_config()
HL_PATH = config['clippings_path']
WORK_PATH = config['work_dir']
MPV_LINES = config['anime_lines_path']
GEN_MEDIA = config['gen_media']
HL_DELIM = "=========="
HL_REGEX = "\n?.+\n.+\n\n(.+)"  # regex to skip metadata
KINDLE_CSV = path.join(WORK_PATH, 'kindle.csv')
MPV_CSV = path.join(WORK_PATH, 'mpv.csv')
MPV_DELIM = "<====>"
LINE_SEP = "[====]\n"


def to_csv(lines):
    # turn the highlights into a tab separaeted csv file
    output = []
    for line in lines:
        output.append(line.strip() + '\t' + '[  ]' + '\t' + '{}')

    return '\n'.join(output)


def kindle():
    with open(HL_PATH, 'r', encoding='utf-8') as f:
        text = f.read()

    lines = text.split(HL_DELIM)
    while '' in lines:
        lines.remove('')
    while '\n' in lines:
        lines.remove('\n')
    highlights = []
    for line in lines:
        hl = re.findall(HL_REGEX, line)[0]
        highlights.append(hl)

    return highlights


def mpv():
    with open(MPV_LINES, 'r', encoding="UTF-8") as f:
        lines = f.read().split(LINE_SEP)
    # remove blank lines
    lines = [line for line in lines if line.split(MPV_DELIM)[0]]
    if GEN_MEDIA:
        htmllines = []
        jpgmp3s = media_gen.gen(lines)
        for i, line in enumerate(lines):
            jpg, mp3 = jpgmp3s[i]
            html = '<img src="{}"><br>[sound:{}]<br>'.format(jpg, mp3)
            htmlline = html + line
            htmllines.append(htmlline)
        lines = htmllines

    return [line.split(MPV_DELIM)[0] for line in lines]


if sys.argv[1] == "kindle":
    lines = kindle()
    csv = to_csv(lines)
    with open(KINDLE_CSV, 'w', encoding='utf-8') as f:
        f.write(csv)

if sys.argv[1] == "mpv":
    lines = mpv()
    csv = to_csv(lines)
    with open(MPV_CSV, 'w', encoding='utf-8') as f:
        f.write(csv)
