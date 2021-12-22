import sys
import json
import re
import config_reader
from os import path as path


config = config_reader.get_config()
WORK_PATH = config['work_dir']
KINDLE_CSV = path.join(WORK_PATH, 'kindle.csv')
MPV_CSV = path.join(WORK_PATH, 'mpv.csv')
DICTIONARY = config['epwing.json']


def save_to(rows, output_csv):
    with open(output_csv, 'w', encoding='UTF-8') as f:
        f.write('\n'.join(rows))


def gen_card_csv(csv, dictionary):
    with open(csv, 'r', encoding='utf-8') as f:
        rows = f.read().split('\n')

    newrows = []
    for row in rows:
        if not row:
            continue
        line, words, extra = row.split('\t')
        words = words.replace('[', '').replace(']', '')

        if ',' in words:
            words = words.split(',')
            words = [w.strip() for w in words]
        else:
            words = [words.strip()]
        for i, word in enumerate(words):
            if re.findall(r'\s+', word) or word == '':
                words[i] = 'NOT FOUND'

        for word in words:
            entry = dictionary[word] if word in dictionary else ''
            if entry and type(entry) == str:
                defs = entry.replace('\n', '<br>')
                newrow = line + '\t' + word + '\t' + defs
            if entry and type(entry) == list:
                defs = '<br><br>'.join(entry)
                defs = defs.replace('\n', '<br>')
                newrow = line + '\t' + word + '\t' + defs
            if not entry:  # nothing found
                newrow = line + '\t' + word + '\t' + '{}'

            newrows.append(newrow)

    return newrows


with open(DICTIONARY, 'r', encoding='utf-8') as f:
    prepared_epwing = json.loads(f.read())

if sys.argv[1] == 'mpv':
    newrows = gen_card_csv(MPV_CSV, prepared_epwing)
    save_to(newrows, MPV_CSV)
if sys.argv[1] == 'kindle':
    newrows = gen_card_csv(KINDLE_CSV, prepared_epwing)
    save_to(newrows, KINDLE_CSV)
