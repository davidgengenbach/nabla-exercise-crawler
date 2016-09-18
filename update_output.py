#!/usr/bin/env python3
import json
import helper

with open('output/exercises.json', 'w+') as f:
    json.dump([folder for folder in helper.get_folders_in_dir('output') if folder != 'lib'], f)