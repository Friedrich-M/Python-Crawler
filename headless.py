from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time
import csv

chrome_options = Options()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
web = Chrome(options=chrome_options)

web.get("https://www.endata.com.cn/BoxOffice/BO/Year/index.html")

# 定位到下拉列表
sel_el = web.find_element(By.XPATH, '//*[@id="OptionDate"]')
# 对元素进行包装， 包装成下拉列表
sel = Select(sel_el)
# 让浏览器进行调整选项
for i in range(len(sel.options)):  # i就是每一个下拉框列表选项的索引位置
    sel.select_by_index(i)  # 按照索引进行切换
    print(f"正在抓取{2022-i}年的电影票房数据")
    time.sleep(1)
    table = web.find_element(By.XPATH, '//*[@id="TableList"]/table')
    f = open('./movie_rank/'+f'Year{2022-i}.csv', mode='w', encoding='utf-8')
    csv_writer = csv.writer(f)
    items = web.find_elements(By.XPATH, '//*[@id="TableList"]/table/thead/tr/th')[1:]
    titles = []
    for item in items:
        titles.append(item.text)
    csv_writer.writerow(titles)
    tbodys = web.find_elements(By.XPATH, '//*[@id="TableList"]/table/tbody/tr')
    for tbody in tbodys:
        datas = tbody.find_elements(By.XPATH, './td')[1:]
        for i, v in enumerate(datas):
            datas[i] = datas[i].text
        csv_writer.writerow(datas)


print("完成任务！")
web.close()

# 如何拿到页面代码Elements（经过数据加载以及js执行之后的结果的html内容）
print(web.page_source)
