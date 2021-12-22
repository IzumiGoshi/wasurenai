import json
import re
import sys

"""
    run with python3 epwing.json outputname.json

    This script takes in an json file created by
    zero epwing. the script then pulls apart the
    entires. ex     "heading": "さらまわし【皿回し】サラマハシ[3]"
    will have new entries made for
    さらまわし, 皿回し, and サラマハシ
"""


char_ranges = {
    'hiragna': [ord(u"\u3040"), ord(u"\u309F")],
    'katakana': [ord(u"\u30A0"), ord(u"\u30FF")],
    'kanji': [ord(u"\u4e00"), ord(u"\u9faf")],
}


def in_range(char_range, c):
    l, u = char_ranges[char_range]
    return ord(c) >= l and ord(c) <= u


def check_for(char_range, s):
    return True in [in_range(char_range, c) for c in s]


def key_split(heading):  # remove brackets
    left = '【'
    right = '】'
    heading = heading.replace('［', left)
    heading = heading.replace('］', left)
    heading = heading.replace(right, left)  # make them all 【

    if left in heading:
        entry = heading.split(left)
    else:
        entry = [heading]

    entries = []
    for e in entry:
        tententen = '…'
        e = e.replace(right, '')
        e = e.replace(':', '')
        e = e.replace(tententen, '')
        for pitch in re.findall(r'\[\d+\]', e):
            e = e.replace(pitch, '')
        for pitch in re.findall(r'\{.+\}', e):
            e = e.replace(pitch, '')

        if e != '':
            entries.append(e)

    return entries


def build_entries(epwing, keys, text):
    assert type(text) == str
    for key in keys:
        if key not in epwing:           # we have an entry
            epwing[key] = text
        elif type(epwing[key]) == str:  # singular text entry
            if text in epwing[key]:
                continue
            epwing[key] = [epwing[key], text]
        else:                           # already multiple entries
            if text in epwing[key]:
                continue
            epwing[key].append(text)


with open(sys.argv[1], 'r', encoding='utf-8') as f:
    epwing_json = f.read()

epwing_json = json.loads(epwing_json)
epwing_json = epwing_json['subbooks']
epwing_json = epwing_json[0]
epwing_json = epwing_json['entries']


epwing = {}
out = []
for se in epwing_json:
    heading = se['heading']
    if 'text' in se:
        text = se['text']
    else:
        text = 'no definition'

    keys = key_split(heading)

    for key in keys:
        build_entries(epwing, keys, text)


textver = json.dumps(epwing, indent=4, ensure_ascii=False).encode('utf-8')
iname = ''.join(sys.argv[1].split('.')[:-1])
with open(sys.argv[2], 'wb') as f:
    f.write(textver)
