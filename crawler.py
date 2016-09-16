from ghost import Ghost
import sys
import os
import json
import requests
import re
import hashlib
import helper

# This is a mess :(

DOMAIN = 'nabla.algo.informatik.tu-darmstadt.de'
BASE_URL = 'https://{}'.format(DOMAIN)
EXERCISE_URL = '{}/genex/exercise/8'.format(BASE_URL)

template = helper.get_template('exercise-template.html')

def sanitize(s):
    return s.replace('\n', ' ').replace('\t', '').strip()

def save_exercise_data(ex_id, data, output_folder = 'output'):
    folder = "{}/{}".format(output_folder, ex_id)
    os.mkdir(folder)
    json_filename = "{}/data.json".format(folder)
    with open(json_filename, 'w+') as f:
        json.dump(data, f, indent = 4)
    # Download images
    os.mkdir("{}/images".format(folder))
    for r in data:
        img = "{}/{}".format(BASE_URL, r['img'])
        filename = r['img_local']
        svg = requests.get(img, verify=False).content
        svg = helper.highlight_nodes(svg, r['highlighted_nodes']).replace('viewbox', 'viewBox')
        with open("{}/{}".format(folder, "images/{}".format(filename)), 'w+') as f:
            f.write(svg)
    # Create HTML
    with open('{}/index.html'.format(folder), 'w+') as f:
        f.write(template.render(id=ex_id, data=data))

ghost = Ghost()
session = ghost.start()
session.load_cookies(helper.get_cookies())
def get_exercise_data(exercise_url):
    page, extra_resources = session.open(exercise_url)

    exercise_id = page.url.replace(exercise_url + '/', '').encode('utf-8')
    exercise_id = hashlib.sha224(exercise_id).hexdigest()

    SCRIPT_SUBMIT_EXERCISE = """
        try {
            jQuery('button#prepareBtn').click();
        } catch(e) { }
        setTimeout(function() {
            jQuery('button[type=\"submit\"]').click()
        }, 200);
    """

    page, resources = session.evaluate(SCRIPT_SUBMIT_EXERCISE, expect_loading=True)
    SCRIPT_GET_EXERCISE_DATA = """
        jQuery('.panel')
            .find('button')
            .remove()
            .end()
            .map(function() {
                var $el = jQuery(this);
                var script = $el.find('script').remove().html();
                return {
                    title: $el.find('.panel-title').text(),
                    script: script,
                    text: $el.find('.panel-body').text().trim(),
                    img: $el.find('object').attr('data')
                }
            }).toArray();
    """

    result, resources = session.evaluate(SCRIPT_GET_EXERCISE_DATA)
    for r in result:
        r['title'] = sanitize(r['title'])
        r['text'] = sanitize(r['text'])
        r['img_local'] = r['img'].split('/')[-1]
        r['highlighted_nodes'] = []
        r['id'] = exercise_id
        if 'script' in r:
            matches = re.findall(r'\$\(this\).text\(\) == "(.*?)"(.*?)\)\n', r['script'])
            for match in matches:
                node = match[0]
                if(match[1] == ''):
                    r['highlighted_nodes'].append(node)
                else:
                    # Test whether this node has to be highlighted too
                    val = match[1].replace('&&', '').split('!=')
                    if(val[0].strip() != val[1].strip()):
                        r['highlighted_nodes'].append(node)

    return (exercise_id, [x for x in result if 'Korrektur' not in x['title']])

ex_id, data = get_exercise_data(EXERCISE_URL)
save_exercise_data(ex_id, data)
