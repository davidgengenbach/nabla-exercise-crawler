import os
import json
import sys

d='output'
directories = ([os.path.join(d,o).replace(d + '/', '') for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))])
with open('output/exercises.json', 'w+') as f:
    json.dump(directories, f)