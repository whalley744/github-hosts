#!/usr/bin/env python3
# _*_coding:utf-8_*_
# author:Whalley

import requests
from flask import Flask
from lxml import etree
import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')
ip_address_com = '.ipaddress.com'


@app.route("/")
def index():
    return '<h2>Hello,World!'


@app.route("/fetch")
def fetch_ip():
    github_url_list = app.config['GITHUB_URL_LIST']
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    host_result = ['# GitHub Host Start\n\n']
    for url in github_url_list:
        fetch_url = build_fetch_url(url)
        try:
            result = requests.get(fetch_url).content.decode('utf-8')
            tree = etree.HTML(result)
            i = 1
            while i < 5:
                tds = tree.xpath(f'//tbody[@id="dnsinfo"]/tr[{i}]/td//text()')
                if tds[1] == 'A':
                    host_result.append(f"{tds[2].ljust(30, ' ')}{url}\n")
                    break
                i = i + 1
        except Exception as ex:
            print(ex)
    host_result.append(f'\n# Update Time: {current_date}')
    host_result.append('\n# GitHub Host End')
    return ''.join(host_result)


def build_fetch_url(url: str) -> str:
    url_splits = url.split('.')
    url_splits_len = len(url_splits)
    if url_splits_len <= 2:
        return f'https://{url}{ip_address_com}'
    return f'https://{url_splits[url_splits_len - 2]}.{url_splits[url_splits_len - 1]}{ip_address_com}/{url}'


if __name__ == "__main__":
    app.run()
