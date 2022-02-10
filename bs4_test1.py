import requests
from bs4 import BeautifulSoup
import csv

url = "http://www.whbsz.com.cn/Price.aspx"
headers = {
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.99 Safari/537.36 '
}

# 构建列表头
f = open('菜价.csv', mode='w', encoding="utf-8")
csv_writer = csv.writer(f)
csv_writer.writerow(["品名", "最高价", "最低价", "均价"])
for page_id in [0, 2]:
    param = {
        "PageNo" : f'{page_id}'
    }
    resp = requests.get(url, headers=headers, params=param)

    # 1.把页面源代码交给BeautiSoup进行处理，生成bs对象
    page = BeautifulSoup(resp.text, "html.parser")  # 指定html解析器
    # 2.从bs对象中查找数据
    table = page.find_all("table", attrs={"cellpadding": "0", "cellspacing": "0",
                                          "width": "100%", "border": "0"})
    # 拿到数据行
    trs = table[4].find_all("tr")[0:]

    for tr in trs:  # 每一行
        tds = tr.find_all("td")[0:]  # 拿到每行中的所有td
        name = tds[0].text.strip()
        high = tds[2].text.strip()
        low = tds[3].text.strip()
        avg = tds[4].text.strip()
        csv_writer.writerow([name, high, low, avg])


f.close()
