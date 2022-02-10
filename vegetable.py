# 1. 如何提取单个页面的数据
# 2. 上线程池， 多个页面同时抓取
import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor

f = open('data.csv', mode='w', encoding='utf-8')
csv_writer = csv.writer(f)
csv_writer.writerow(["品名", "最高价", "最低价", "均价"])

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/97.0.4692.71 " \
                  "Safari/537.36 "
}


def download_one_page(url):
    # 拿到页面源代码
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    html = etree.HTML(resp.text)
    table = html.xpath("/html/body/form/table[4]/tr/td[3]/table[5]")[0]
    trs = table.xpath("./tr")
    for tr in trs:
        text = tr.xpath("./td[position()!=2]/text()")
        # 对数据进行简单的处理
        text = list(item.replace("\xa0", "") for item in text)
        csv_writer.writerow(text)


if __name__ == "__main__":
    # url = "http://www.whbsz.com.cn/Price.aspx"
    # download_one_page(url)

    with ThreadPoolExecutor(22) as t:
        for i in range(1, 3):
            t.submit(download_one_page, url=f'http://www.whbsz.com.cn/Price.aspx?PageNo={i}')

