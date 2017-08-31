# -*- coding:utf-8 -*-
__author__ = 'lius'

import requests
import re
import json
import os

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
        }
    session = requests.session()
    html = str(session.get(url,headers=headers).content,encoding='gbk')
    return html

def parser_home_page(url):
    html = get_html(url)
    html_type_dict = json.loads(html)
    url_list = []
    for info in html_type_dict["data"]["searchDOList"]:
        url_list.append({"userUrl": "https://mm.taobao.com/self/aiShow.htm?userId=" + str(info["userId"]), "name": info["realName"], 'city': info["city"]})
    return url_list

def parser_mm_page(user_info):
    print(user_info)
    html = get_html(user_info["userUrl"])
    pattern = re.compile(r'<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
    data = re.findall(pattern, html)
    patternImg = re.compile('<img.*?src="(.*?)"', re.S)
    images = re.findall(patternImg, data[0])
    for url in images:
        download_image(user_info["name"]+ '.' +user_info["city"], 'http:'+url, user_info["name"])

def download_image(name, url, folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    filename = folder + '/' + name + '.' +url.split("/")[-1]
    print(filename)
    r = requests.get(url)
    with open(filename, "wb") as code:
        code.write(r.content)

if __name__ == "__main__":
    mms_info = parser_home_page("https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8")
    for mm_info in mms_info:
        parser_mm_page(mm_info)
    print("--END--")