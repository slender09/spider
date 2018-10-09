# -*- coding: utf-8 -*-

import urllib.request
import re, json, os

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    if response.status == 200:
        return response.read().decode('utf-8')
    return None
    


def parse_one_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3])>3 else '',
            'time': item[4].strip()[5:] if len(item[4])>5 else '',
            'score': item[5].strip()+item[6].strip()
        }

def write_to_file(content):

    with open('result.txt', 'a', encoding = 'utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+'\n')

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)

    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    if os.path.exists('result.txt'):
        os.remove('result.txt')
    for i in range(10):
        main(i*10)