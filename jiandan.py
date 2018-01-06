# !/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import os
from Download import request
import threading
import requests
import hashlib   
import base64
import re
import random
import shutil

def parse (imgHash, constant): 
    q = 4
    hashlib.md5()   
    constant = md5(constant)
    o = md5(constant[0:16])
    n = md5(constant[16:32])    
    l = imgHash[0:q]
    c = o + md5(o + l)
    imgHash = imgHash[q:]
    k = decode_base64(imgHash)
    h =list(range(256))

    b = list(range(256))

    for g in range(0,256):
        b[g] = ord(c[g % len(c)])

    f=0
    for g in range(0,256):
        f = (f+h[g]+b[g]) % 256
        tmp = h[g]
        h[g] = h[f]
        h[f] = tmp
        
    result = ""
    p=0
    f=0
    for g in range(0,len(k)):   
        p = (p + 1) % 256
        f = (f + h[p]) % 256
        tmp = h[p]
        h[p] = h[f]
        h[f] = tmp
        result += chr(k[g] ^ (h[(h[p] + h[f]) % 256]))
    result = result[26:]
    
    return result

def md5(src):
    m = hashlib.md5()   
    m.update(src.encode("utf8"))  
    return m.hexdigest()

def decode_base64(data):
    missing_padding=4-len(data)%4
    if missing_padding:
        data += '='* missing_padding
    return base64.b64decode(data)

headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'jandan.net',
    'Referer':'http://jandan.net/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

url = 'http://jandan.net/ooxx/page-{}#comments'.format(3)
html = request.get(url, 3).text
j=re.search(r'.*<script\ssrc=\"\/\/(cdn.jandan.net\/static\/min.*?)\"><\/script>.*',html)
jsFileUrl="http://"+j.group(1)
jsFile=requests.get(jsFileUrl,headers=headers).text

index = 0
class jiandan():
    def get(self, url):
        html = request.get(url, 3)
        return html.text
    def save(self, url):
        global index
        global jsFile
        html = self.get(url)
        soup = BeautifulSoup(html, 'lxml')
        # tag_all = soup.find_all('div', class_='text')

        c=re.search(r'.*f_\w+\(e,\"(\w+)\".*',jsFile)
        constant=c.group(1)

        resultList=[]
        for item in soup.select('.img-hash'):
            resultList.append(item.text)
        for result in resultList:
            # img_url =  tag.text;
            url='http:'+parse(result,constant)
            replace = re.match(r'(.*\.sinaimg\.cn\/)(\w+)(\/.+\.gif)', url)
            if replace:
                url = replace.group(1) + 'large' + replace.group(3)
            e = re.match(r'.*(\.\w+)', url)
            extensionName = e.group(1)
            with open(str(index) + extensionName, 'wb') as f:
                index = index+1
                headers['host'] = 'wx3.sinaimg.cn'
                f.write(requests.get(url, headers=headers).content)
                f.close()



for i in range(3, 9):
    url = 'http://jandan.net/ooxx/page-{}#comments'.format(i)
    print (url)
    jd = jiandan()
    jd.save(url)
