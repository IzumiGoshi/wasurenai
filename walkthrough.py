import sys
import os

if len(sys.argv) < 2 or sys.argv[1] not in ['mpv', 'kindle']:
    print('run this script with either "mpv" or "kindle" as an argument')
    sys.exit()

source = sys.argv[1]
print('running csv_maker.py')
print('if you haven\'t set up your config.json check the readme')

os.system('python3 csv_maker.py ' + source)
input('open up the csv and add the words to define inside the [  ]')
os.system('python3 definition_gen.py ' + source)
print('done. import the csv into anki')
print('make sure you toggle allow html')
