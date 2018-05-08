import requests
import re
import time
import pandas as pd
import urllib.request
from lxml import etree
from douban import ip_proxy

all_types_names = []
all_types_urls = []
n = 0

print('开始读取'+'\n')
print('……')
begin_url = 'https://movie.douban.com/chart'
# 读取排行榜起始页的源代码，调用ip_proxy，实现伪装读取
# urllib.request.install_opener(ip_proxy.opener)
# begin_url_html=urllib.request.urlopen(begin_url).read().decode('utf-8')
# 未调用前
begin_url_html = requests.get(begin_url).text
print('……')
movies_types_urls = re.findall('<span><a href="(.*?)">', begin_url_html)
# print(movies_types_urls)
print('……')
for every_types_url in movies_types_urls:
    movies_types_name = re.findall('type_name=(.*?)&type', every_types_url)[0]
    all_types_names.append(movies_types_name)
    type_number=re.findall('&type=(.*?)&interval',every_types_url)[0]
    types_urls = 'https://movie.douban.com' + every_types_url
    print('……'+'\n')
    allrank = []
    alltypes = []
    alltitle = []
    allurl = []
    allregions = []
    allrelease_date = []
    allactor_count = []
    allmain_actor = []
    allvote_count = []
    allscore = []

    urls = []
    for i in range(100, 0, -10):
        url1 = 'https://movie.douban.com/j/chart/top_list_count?type='+type_number+'&interval_id=' + str(i) + '%3A' + str(i - 10)
        urls.append(url1)  # print(url)
    for ten_per_amount_url in urls:
        per_a = re.findall('interval_id=(.*?)%3A', ten_per_amount_url)[0]
        per_b = str(int(per_a) - 10)
        # 读取该10%的电影中的数量值
        urllib.request.install_opener(ip_proxy.opener)
        per_amount_html=urllib.request.urlopen(ten_per_amount_url).read().decode('utf-8')
        #未调用前 per_amount_html = requests.get(ten_per_amount_url).text
        per_amount = re.findall('"total":(.*?),"unwatched_count', per_amount_html)[0]
        print('正输出类型为：' + movies_types_name + '\n' + per_a + '%至' + per_b + '%的电影' + '\n' + '本类型该10%中共计：' + str(
            per_amount) + '部电影')

        n = 0
        # a=ten_percent_movie_amount
        for a in range(0, int(per_amount) + 1, 20):
            movies_url = 'https://movie.douban.com/j/chart/top_list?type='+type_number+'&interval_id=' + per_a + '%3A' + per_b + '&action=&start=' + str(
                a) + '&limit=20'
            movies_url_html = requests.get(movies_url).text
            plot_film = re.findall('"rating"(.*?)'"is_watched", movies_url_html)
            # time.sleep(1)
            for every_film in plot_film:
                n = n + 1
                rating = re.findall('\\["(.*?)",', every_film)[0]
                types = re.findall('"types":\\["(.*?)"\\],', every_film)[0].replace(',', '').replace('""', "|")
                regions = re.findall('"regions":\\["(.*?)"\\],', every_film)[0].replace(',', '').replace('""', "|")
                title = re.findall('"title":"(.*?)"', every_film)[0]
                url = re.findall('"url":"(.*?)"', every_film)[0].replace('\\', '')
                release_date = re.findall('"release_date":"(.*?)"', every_film)[0]
                actor_count = re.findall('"actor_count":(.*?),"vote_count"', every_film)[0]
                vote_count = re.findall('"vote_count":(.*?),"score"', every_film)[0]
                score = re.findall('"score":"(.*?)"', every_film)[0]

                b = int(actor_count)
                actors = re.findall('"actors":\\[(.*?)\\],', every_film)
                main_actors = re.findall('"(.*?)"', actors[0])
                if b == 0:
                    main_actor = '无主要演员'
                elif b == 1:
                    main_actor = main_actors[0]
                elif b == 2:
                    main_actor = main_actors[0] + '|' + main_actors[1]
                else:
                    main_actor = main_actors[0] + '|' + main_actors[1] + '|' + main_actors[2]

                allrank.append(n)
                alltypes.append(types)
                alltitle.append(title)
                allurl.append(url)
                allregions.append(regions)
                allrelease_date.append(release_date)
                allactor_count.append(actor_count)
                allmain_actor.append(main_actor)
                allvote_count.append(vote_count)
                allscore.append(score)

                # print('rank：' + str(n))
                # print('类型：' + types)
                # print('标题：' + title)
                # print('内容页网址：' + url)
                # print('国家：' + regions)
                # print('日期：' + release_date)
                # print('演员数：' + actor_count)
                # print('主演：' + main_actor)
                # print('评价数：' + vote_count)
                # print('分数：' + score)
                # print('\n')
                # time.sleep(0.5)

            print('已读入第' + str(a) + '至' + str(a + 20) + '部电影')
        print(per_a + '%至' + per_b + '的电影读入' + '\n')

    data1 = pd.DataFrame({'rank': allrank,
                          'types': alltypes,
                          'title': alltitle,
                          'url': allurl,
                          'regions': allregions,
                          'release_date': allrelease_date,
                          'actor_count': allactor_count,
                          'main_actor': allmain_actor,
                          'vote_count': allvote_count,
                          'score': allscore})

    data1.to_csv(u'movie' + movies_types_name + '.csv', index=False, encoding='"utf_8_sig')
    print(movies_types_name + '的电影信息已完成.')
    # time.sleep(3)
