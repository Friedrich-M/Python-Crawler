from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(options=chrome_options)

browser.get("https://music.163.com/#/song?id=1914696104")

time.sleep(2)

try:
    browser.switch_to.frame('g_iframe')  # 记得切换到所要找的元素所在的frame，不然会找不到元素，这里有的网页不需要切换，所以使用try
except:
    pass

song_name = browser.find_element(By.XPATH, '//div[@class = "tit"]/em')
print(song_name.text)
items = browser.find_elements(By.XPATH,
                              '//div[@class = "cmmts j-flag"]//div[@class = "cntwrap"]/div/div[@class '
                              '= "cnt f-brk"]')
for item in items:
    print(item.text.strip('\n'))



