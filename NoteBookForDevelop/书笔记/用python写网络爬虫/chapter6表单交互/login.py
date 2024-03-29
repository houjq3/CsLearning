# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import urllib.parse
import glob
import sqlite3
import os
import http.cookiejar
import json
import time
import lxml.html

# TODO: 没有测试

LOGIN_EMAIL = '1040003585@qq.com'
LOGIN_PASSWORD = 'wu.com'
#LOGIN_URL = 'http://example.webscraping.com/user/login'
LOGIN_URL = 'http://127.0.0.1:8000/places/default/user/login'
COUNTRY_URL = 'http://example.webscraping.com/edit/United-Kingdom-239'


def login_basic():
    """fails because not using formkey
    """
    data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
    encoded_data = urllib.parse.urlencode(data)
    request = urllib.request.Request(LOGIN_URL, encoded_data)
    response = urllib.request.urlopen(request)
    print(response.geturl())


def login_formkey():
    """fails because not using cookies to match formkey
    """
    html = urllib.request.urlopen(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.parse.urlencode(data)
    request = urllib.request.Request(LOGIN_URL, encoded_data)
    response = urllib.request.urlopen(request)
    print(response.geturl())


def login_cookies():
    """working login
    """
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj))
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.parse.urlencode(data)
    request = urllib.request.Request(LOGIN_URL, encoded_data)
    response = opener.open(request)
    print(response.geturl())
    return opener


def login_firefox():
    """load cookies from firefox
    """
    session_filename = find_ff_sessions()
    cj = load_ff_sessions(session_filename)
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj))
    html = opener.open(COUNTRY_URL).read()

    tree = lxml.html.fromstring(html)
    print(tree.cssselect('ul#navbar li a')[0].text_content())
    return opener


def parse_form(html):
    """extract all input properties from the form
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def load_ff_sessions(session_filename):
    cj = http.cookiejar.CookieJar()
    if os.path.exists(session_filename):
        try:
            json_data = json.loads(open(session_filename, 'rb').read())
        except ValueError as e:
            print('Error parsing session JSON:', str(e))
        else:
            for window in json_data.get('windows', []):
                for cookie in window.get('cookies', []):
                    import pprint
                    pprint.pprint(cookie)
                    c = http.cookiejar.Cookie(0, cookie.get('name', ''), cookie.get('value', ''),
                                              None, False,
                                              cookie.get('host', ''), cookie.get('host', '').startswith(
                                                  '.'), cookie.get('host', '').startswith('.'),
                                              cookie.get('path', ''), False,
                                              False, str(
                                                  int(time.time()) + 3600 * 24 * 7), False,
                                              None, None, {})
                    cj.set_cookie(c)
    else:
        print('Session filename does not exist:', session_filename)
    return cj


def find_ff_sessions():
    paths = [
        '~/.mozilla/firefox/*.default',
        '~/Library/Application Support/Firefox/Profiles/*.default',
        '%APPDATA%/Roaming/Mozilla/Firefox/Profiles/*.default'
    ]
    for path in paths:
        filename = os.path.join(path, 'sessionstore.js')
        matches = glob.glob(os.path.expanduser(filename))
        if matches:
            return matches[0]


def main():
    # login_basic()
    # login_formkey()
    login_cookies()
    # login_firefox()


if __name__ == '__main__':
    main()
