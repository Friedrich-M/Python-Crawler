import requests
from lxml import etree

url = "https://tz.zbj.com/search/f/?kw=saas"
resp = requests.get(url)

# 解析
html = etree.HTML(resp.text)

# 拿到每一个服务商的div
divs = html.xpath("/html/body/div[6]/div/div/div[2]/div[5]/div[1]/div")
for div in divs:
    price = div.xpath('./div/div/a[2]/div[2]/div[1]/span[1]/text()')[0].strip('¥')
    title = "saas".join(div.xpath('./div/div/a[2]/div[2]/div[2]/p/text()'))
    com_name = div.xpath('./div/div/a[1]/div[1]/p/text()')[1].strip('\n')
    location = div.xpath('./div/div/a[1]/div[1]/div/span/text()')[0]
    print(price, title, com_name, location, sep=' ')









