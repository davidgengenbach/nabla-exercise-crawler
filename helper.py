from bs4 import BeautifulSoup
import re
from jinja2 import Template
import http.cookiejar

def get_cookies(filename = 'cookies.txt'):
    jar = http.cookiejar.CookieJar()
    cookies = []
    with open(filename, 'r') as f:
        for line in f:
            cookie = line.strip()
            if cookie != '':
                matches = re.findall(r'(.*?)\s{2,3}', cookie.strip())
                secure = len(matches) > 4 and matches[4] != None
                domain = matches[2]
                domain_initial_dot = False
                if domain[0] == '.':
                    domain = domain[1:]
                    domain_initial_dot = True
                #'version', 'name', 'value', 'port', 'port_specified', 'domain', 'domain_specified', 'domain_initial_dot', 'path', 'path_specified', 'secure', 'expires', 'discard', 'comment', 'comment_url', and 'rest'
                # Don't know why this is so complicated...
                c = http.cookiejar.Cookie(None, matches[0], matches[1], '80', '80', domain, domain_initial_dot, None, matches[3], None, secure, False, None, None, None, None)
                cookies.append(c)

    for cookie in cookies:
        jar.set_cookie(c)
    return jar

def get_template(file):
    with open(file, 'r') as f:
        return Template(f.read())

def highlight_nodes(svg_image, highlighted_nodes):
    soup = BeautifulSoup(svg_image, 'html.parser')
    for title in soup.select('.node title'):
        for index, node in enumerate(highlighted_nodes):
            if node in title:
                pol = title.parent.find('polygon')
                colors = ['lime', 'blue']
                pol.attrs['style']  = "stroke: {}; stroke-width: {}".format(colors[index % 2], 3)
    return str(soup)