#!/usr/bin/python
# coding:utf-8
import requests
import json
import codecs
import sys
import re
from numconverter import cn2dig
import os

def startcrawl(pageurl):
    response = requests.request('GET', pageurl)
    content = response.content
    if content[:3] == codecs.BOM_UTF8:
        content = content[3:]
        content = content.strip()
    text = content.decode()
    results = re.search('\$\.get\(\'/novelsearch/.*\',\{siteid:\'(\d+)\',url:\'(.*)\'}', text, re.IGNORECASE)
    siteid = results.groups(0)[0]
    geturl = results.groups(0)[1]
    nexturl = re.search('var nextpage = "(.+) *\" *;\n', text, re.IGNORECASE).groups(0)[0]

    try:
        finalresponse = requests.get('http://www.doupocangqiong1.com/novelsearch/reader/transcode.html', {'siteid': siteid, 'url': geturl})
        finaltxt = finalresponse.content
        if finaltxt[:3] == codecs.BOM_UTF8:
            finaltxt = finaltxt[3:]
            finaltxt = finaltxt.strip()
        finaltxt = finaltxt.decode()
        novel_data = json.loads(finaltxt)
        novel_txt = novel_data['info']
        novel_txt = novel_txt.replace('<br/>', '\r\n')
        novel_txt = novel_txt.replace('(未完待续)', '')
        novel_txt = re.sub('\((.*\n)*?.*\)$', '', novel_txt)
        novel_txt = re.sub('(\r*\n)+', '\r\n', novel_txt)

        try:
            title_results = re.search('([第地][一二两三四五六七八九十百千万]+章 .+) *- 斗破苍穹 *-', text, re.IGNORECASE)
            if not title_results is None:
                title_results =title_results.groups(0)[0]
                title_index = re.search('[第地]([一二两三四五六七八九十百千万]+)章 ', title_results, re.IGNORECASE).groups(0)[0].strip()
                title_text = re.search('[第地][一二两三四五六七八九十百千万]+章 (.*)', title_results, re.IGNORECASE).groups(0)[0]
                digit_index = cn2dig(title_index)
                txt_name = str(digit_index) + ' ' + title_text
            else:
                title_results = re.search('([第地][一二两三四五六七八九十百千万]+章* .+) *- 斗破苍穹 *-', text, re.IGNORECASE)
                if not title_results is None:
                    title_results = title_results.groups(0)[0].strip()
                    title_index = re.search('[第地]([一二两三四五六七八九十百千万]+)章* ', title_results, re.IGNORECASE).groups(0)[0].strip()
                    title_text = re.search('[第地][一二两三四五六七八九十百千万]+章* (.*)', title_results, re.IGNORECASE).groups(0)[0]
                    digit_index = cn2dig(title_index)
                    txt_name = str(digit_index) + ' ' + title_text
                else:
                    title_results = re.search('([第地]*[一二两三四五六七八九十百千万]+章 .+) *- 斗破苍穹 *-', text, re.IGNORECASE)
                    if not title_results is None:
                        title_results = title_results.groups(0)[0].strip()
                        title_index = re.search('[第地]*([一二两三四五六七八九十百千万]+)章 ', title_results, re.IGNORECASE).groups(0)[0].strip()
                        title_text = re.search('[第地]*[一二两三四五六七八九十百千万]+章 (.*)', title_results, re.IGNORECASE).groups(0)[0]
                        digit_index = cn2dig(title_index)
                        txt_name = str(digit_index) + ' ' + title_text
                    else:
                        title_results = re.search('([第地][一二两三四五六七八九十百千万]+章 .+)"><i', text, re.IGNORECASE)
                        title_results = title_results.groups(0)[0].strip()
                        title_index = re.search('[第地]*([一二两三四五六七八九十百千万]+)章 ', title_results, re.IGNORECASE).groups(0)[0].strip()
                        title_text = re.search('[第地]*[一二两三四五六七八九十百千万]+章 (.*)', title_results, re.IGNORECASE).groups(0)[0]
                        digit_index = cn2dig(title_index)
                        txt_name = str(digit_index) + ' ' + title_text
            writenovel(txt_name, novel_txt)
        except Exception:
            print('get title exception:' + nexturl)
    except Exception:
        print('get novel exception:' + nexturl)
        #writenovel('exception', nexturl)
        except_f = open('E:/exceptfile.txt', 'a')
        except_f.write(nexturl)
        except_f.close()
    return nexturl

def writenovel(novel_name, novel_content):
    f = open('E:/doupocangqiong/' + novel_name + '.txt', 'a')
    f.write(novel_content)
    f.close()

if __name__ == '__main__':
    url_pre = 'http://www.doupocangqiong1.com'
    seed_url = '/1/20.html'
    while seed_url != '/1/1677.html':
        seed_url = startcrawl(url_pre + seed_url)
