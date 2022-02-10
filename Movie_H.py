import requests
import re

domain = "https://www.dydytt.net/index2.htm"
domain1 = "https://www.dydytt.net/"
resp = requests.get(url=domain, verify=False)  # verit=False 去掉安全验证
resp.encoding = 'gb2312'

obj1 = re.compile(r'IMDB评分8分左右影片500余部.*?<br/>(?P<url>.*?)</ul>', re.S)
obj2 = re.compile(r"<a href='(?P<href>.*?)'>", re.S)
obj3 = re.compile(r'◎译　　名(?P<movie>.*?)/', re.S)

child_href_list = []
result1 = obj1.finditer(resp.text)
for it in result1:
    url = it.group("url").strip()

    # 提取子页面链接
    results2 = obj2.finditer(url)
    for itt in results2:
        # 拼接子页面的url地址： 域名 + 子页面地址
        child_href = domain1 + itt.group('href')
        child_href_list.append(child_href)  # 把子页面链接保存起来


# 提取子页面内容
for href in child_href_list:
    child_resp = requests.get(href, verify=False)
    child_resp.encoding = 'gb2312'
    print(child_resp.text)
    break

