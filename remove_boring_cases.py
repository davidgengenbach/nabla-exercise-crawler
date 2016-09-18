#!/usr/bin/env python3
import json
import helper

BORING_CASES = [
    "Der Zeiger p wird auf die Wurzel initialisiert.",
    "Der Zeiger p steigt hinab.",
    "Der aktuelle Knoten ist ein Blatt und es kann einfach eingefügt werden."
]


def get_file_contents(file, mode = 'r+'):
    with open(file, mode) as f:
        return f.read()

exercises = [json.loads(get_file_contents('output/' + folder + '/data.json')) for folder in helper.get_folders_in_dir('output')]

for exercise in exercises:
    is_boring = True
    ID = exercise[0]['id']
    for step in exercise[2:]:
        text = step['text'].strip()
        title = step['title'].strip()
        # One text is all it need to be non-boring
        if text != "" and text not in BORING_CASES:
            is_boring = False

    if is_boring:
        folder = 'output/{}'.format(ID)
        print("Removing boring folder: {}".format(ID))
        helper.remove_folder(folder)
