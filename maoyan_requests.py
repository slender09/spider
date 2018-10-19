# -*- coding: utf-8 -*-

import requests, re
import os, json

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/4.0;(compatible; MSIE 5.5; Windows NT)'
    }
    r = requests.get(url, headers = headers)
    if r.status_code == 200:
        print(r.text)
        return r.text

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

def write2file(content):
    with open('results.txt', 'a', encoding = 'utf-8') as f:
        f.write(json.dumps(content, ensure_ascii = False)+'\n')
        
def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write2file(item)

if __name__ == "__main__":
    if os.path.exists('results.txt'):
        os.remove('results.txt')
    for offset in range(10):
        main(offset*10)