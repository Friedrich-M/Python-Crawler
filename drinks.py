# date：2022.3.5
# author:mlz
# aim:爬取google图片

from selenium import webdriver
import time
import os
import requests
from selenium.webdriver.common.by import By

# 使用代理的方法 ，可以直接windows使用代理，不用这么麻烦
# browserOptions = webdriver.ChromeOptions()
# browserOptions.add_argument('--proxy-server=ip:port)
# browser = webdriver.Chrome(chrome_options=browserOptions)

# 修改keyword便可以修改搜索关键词
keyword = "Blue cube"
url = 'https://www.google.com.hk/search?q=' + keyword + '&tbm=isch'


class Crawler_google_images:
    # 初始化
    def __init__(self):
        self.url = url

    # 获得Chrome驱动，并访问url
    def init_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")

        # 使用headless无界面浏览器模式
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        browser = webdriver.Chrome(options=chrome_options)
        # 访问url
        browser.get(self.url)
        # 最大化窗口，之后需要爬取窗口中所见的所有图片
        browser.maximize_window()
        return browser

    # 下载图片
    def download_images(self, browser, round=2):
        picpath = '蓝方块'
        # 路径不存在时创建一个
        if not os.path.exists(picpath):
            os.makedirs(picpath)
        # 记录下载过的图片地址，避免重复下载
        img_url_dic = []

        count = 0  # 图片序号
        pos = 0
        for i in range(round):
            pos += 500
            # 向下滑动
            js = 'var q=document.documentElement.scrollTop=' + str(pos)
            browser.execute_script(js)
            time.sleep(1)
            # 找到图片
            # html = browser.page_source#也可以抓取当前页面的html文本，然后用beautifulsoup来抓取
            # 直接通过tag_name来抓取是最简单的，比较方便

            img_elements = browser.find_elements(by=By.TAG_NAME, value='img')
            # 遍历抓到的webElement
            for img_element in img_elements:
                img_url = img_element.get_attribute('src')
                # 前几个图片的url太长，不是图片的url，先过滤掉，爬后面的
                if isinstance(img_url, str):
                    if len(img_url) <= 200:
                        # 将干扰的goole图标筛去
                        if 'images' in img_url:
                            # 判断是否已经爬过，因为每次爬取当前窗口，或许会重复
                            # 实际上这里可以修改一下，将列表只存储上一次的url，这样可以节省开销，不过我懒得写了···
                            if img_url not in img_url_dic:
                                try:
                                    img_url_dic.append(img_url)
                                    # 下载并保存图片到当前目录下
                                    filename = "./蓝方块/" + str(count) + ".jpg"
                                    r = requests.get(img_url)
                                    with open(filename, 'wb') as f:
                                        f.write(r.content)
                                    f.close()
                                    count += 1
                                    print('this is ' + str(count) + 'st img')
                                    # 防止反爬机制
                                    time.sleep(0.2)
                                except OSError as e:
                                    print('failure')
                                    print(e)

    def run(self):
        self.__init__()
        browser = self.init_browser()
        self.download_images(browser, 10)  # 可以修改爬取的页面数，基本10页是100多张图片
        browser.close()
        print("爬取完成")


if __name__ == '__main__':
    craw = Crawler_google_images()
    craw.run()
