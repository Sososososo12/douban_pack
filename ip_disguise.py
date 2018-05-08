import re
import requests
from lxml import etree

ip_all=[]
url='http://www.xicidaili.com/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '  
                        'Chrome/51.0.2704.63 Safari/537.36'}
html=requests.get(url,headers=headers).text
# print()
selector=etree.HTML(html)
ip_panel=selector.xpath('//table[@id="ip_list"]' )
ip_amount=ip_panel[0].xpath('tr[@class="odd"]/td/text()')
for n in range(0,68,7):
    ip_all.append(ip_amount[n])
# print(ip_all)
