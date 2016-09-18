from ghost import Ghost
import sys
import os
import json
import requests
import re
import hashlib
import helper
import sys
from exercise_ids import get_exercise_config_from_name

# This is a mess :(

DOMAIN = 'nabla.algo.informatik.tu-darmstadt.de'
BASE_URL = 'https://{}'.format(DOMAIN)

template = helper.get_template('templates', 'exercise-template.html')

def main():
    exercise_name = 'bellman_ford'

    if len(sys.argv) == 2:
        exercise_name = sys.argv[1]
    current_exercise = get_exercise_config_from_name(exercise_name)

    ex_id, data = get_exercise_data(BASE_URL, current_exercise['id'], current_exercise['fill_in'])
    save_exercise_data(ex_id, data)

def get_exercise_url(base_url, exercise_id):
    return '{}/genex/exercise/{}'.format(base_url, exercise_id)

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
        if 'img' in r:
            img = "{}/{}".format(BASE_URL, r['img'])
            filename = r['img_local']
            svg = requests.get(img, verify=False).content
            if 'highlighted_nodes' in r:
                svg = helper.highlight_nodes(svg, r['highlighted_nodes']).replace('viewbox', 'viewBox')
            with open("{}/{}".format(folder, "images/{}".format(filename)), 'w+') as f:
                f.write(svg)
    # Create HTML
    with open('{}/index.html'.format(folder), 'w+') as f:
        f.write(template.render(title='Exercise', id=ex_id, data=data))


def sanitize_html(html):
    return re.sub(r' class="MathJax_Preview">(.*?)<\/', '>$#\g<1>#$<', html)

ghost = Ghost()
session = ghost.start(exclude="\.(css)$")
session.load_cookies(helper.get_cookies())
def get_exercise_data(base_url, exercise_url_id, fill_value_in_inputs = '1'):
    print(exercise_url_id)
    exercise_url = get_exercise_url(base_url, exercise_url_id)
    session.evaluate('window.WebSockets=undefined')
    session.evaluate('window.localStorage=undefined')
    session.evaluate('window.sessionStorage=undefined')
    session.evaluate('window.RTCPeerConnection=undefined')
    session.evaluate('window.webkitRTCPeerConnection=undefined')
    session.evaluate('window.mozRTCPeerConnection=undefined')

    page, extra_resources = session.open(exercise_url)

    exercise_id = page.url.replace(exercise_url + '/', '').encode('utf-8')

    print("\n" * 4)
    print("Exercise ID: {}".format(exercise_id))
    print("\n" * 4)

    exercise_id = hashlib.sha224(exercise_id).hexdigest()

    if fill_value_in_inputs is not None:
        SCRIPT_FILL_TABLE_ENTRIES = '''
            jQuery('#exerciseform td input').val('1');
        '''
        session.evaluate(SCRIPT_FILL_TABLE_ENTRIES)


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
            .filter(function(index) {
                return index < 1;
            })
            .remove()
            .map(function(index) {
                var $el = jQuery(this);
                var script = $el.find('script').remove().html();
                return {
                    title: $el.find('.panel-title').text(),
                    script: script,
                    text: $el.find('.panel-body').text().trim(),
                    img: $el.find('object').attr('data'),
                    html: $el.html()
                }
            })
            .toArray();
    """

    def get_next_results():
        result, resources = session.evaluate(SCRIPT_GET_EXERCISE_DATA)
        return result

    # Get result panels one at a time
    # because ghost.py gets a segmantation fault 11
    # when the result of a session.evaluate is rather big (in this case: a lot of html)
    results = []
    while True:
        result = get_next_results()
        if result == []:
            break
        results = results + result

    for r in results:
        r['title'] = sanitize(r['title'])
        r['text'] = sanitize(r['text'])
        r['img_local'] = r['img'].split('/')[-1] if 'img' in r else None
        r['highlighted_nodes'] = []
        r['id'] = exercise_id

        r['html'] = sanitize_html(r['html'])

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

    return (exercise_id, [x for x in results if 'Korrektur' not in x['title']])


if __name__ == '__main__':
    main()