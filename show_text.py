#!/usr/bin/env python3
import json
import helper

def get_file_contents(file, mode = 'r+'):
    with open(file, mode) as f:
        return f.read()

exercises = [json.loads(get_file_contents('output/' + folder + '/data.json')) for folder in helper.get_folders_in_dir('output')]
for exercise in exercises:
    print("\n\n{}".format(exercise[0]['id']))
    for step in exercise:
        if step['text'].strip() != '' and step['title'].strip() not in ['Aufgabe', 'Lösung']:
            print("{}: {}".format(step['title'], step['text']))