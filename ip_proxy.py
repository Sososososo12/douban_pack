import re
import requests
import urllib.request
from lxml import etree
from douban import ip_disguise
import random

random_ip=random.choice(ip_disguise.ip_all)


url='https://movie.douban.com/chart'
#浏览器伪装
# opener=urllib.request.build_opener()

#设置代理
proxy = {'http': random_ip}
proxy_support = urllib.request.ProxyHandler(proxy)
opener=urllib.request.build_opener(proxy_support)
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
# urllib.request.install_opener(opener)
# html=urllib.request.urlopen(url).read().decode('utf-8')
