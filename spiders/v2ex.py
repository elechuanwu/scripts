# -*- coding: utf-8 -*-
import json
import requests
from bs4 import BeautifulSoup
import time

V2EX_USERNAME = 'chuanwu'
V2EX_PASSWD   = '123456'

headers = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'cache-control':'max-age=0',
    'origin':'https://www.v2ex.com',
    'referer':'https://www.v2ex.com/signin',
    'upgrade-insecure-requests':1,
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
}

def parse_login_page(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    forms = soup.find_all('form')
    for form in forms:
        inputs = form.find_all('input')
        for _input in inputs:
            if u"用户名" in str(_input).decode('utf-8'):
                username = _input.get('name')
            elif "password" in str(_input):
                passwd = _input.get('name')
            elif "once" in str(_input):
                once = _input.get('value')

    return str(username), str(passwd), int(once)

def login_in_v2ex():
    login_url = 'https://www.v2ex.com/signin'
    with requests.Session() as session:
        resp = session.get(login_url, headers=headers)
        time.sleep(1)
        username, passwd, once = parse_login_page(resp.content)
        data = {
                username: V2EX_USERNAME,
                passwd:   V2EX_PASSWD,
                "once": once,
                "next": "/"
        }
        resp = session.post(login_url, data=data, headers=headers)
        print resp.content

login_in_v2ex()

