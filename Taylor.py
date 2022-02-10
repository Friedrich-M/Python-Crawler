from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor  # 多线程
import time


class Taylor(object):
    """
    download the comments
    """

    def __init__(self):
        self.song_urls = []
        self.singer_id = '44266'
        self.singer_url = f'https://music.163.com/#/artist?id={self.singer_id}'

        chrome_options = Options()
        # 使用headless无界面浏览器模式
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # 启动浏览器，获取网页源代码
        self.browser = webdriver.Chrome(options=chrome_options)

    def get_music_url(self):
        self.browser.get(self.singer_url)
        time.sleep(1)
        try:
            self.browser.switch_to.frame('g_iframe')
        except:
            pass
        items = self.browser.find_elements(By.XPATH, '//table[@class = "m-table m-table-1 '
                                                     'm-table-4"]/tbody/tr//span[@class = "txt"]/a')
        for item in items:
            href = item.get_attribute('href')
            self.song_urls.append(href)
            # print("要爬取的地址有： ", href)

    def get_comments(self):
        for url in self.song_urls:
            self.browser.get(url)
            time.sleep(1)
            try:
                self.browser.switch_to.frame('g_iframe')
            except:
                pass
            song_name = self.browser.find_element(By.XPATH, '//div[@class="tit"]/em').text
            comments = self.browser.find_elements(By.XPATH, '//div[@class = "cmmts j-flag"]//div[@class = '
                                                            '"cntwrap"]/div/div[@class = "cnt f-brk"]')

            print(f"正在抓取{song_name}")
            # 将下载的评论写入文件
            with open("comments/" + song_name + '.txt', mode='a+', encoding='utf-8') as f:
                for comment in comments:
                    f.write(comment.text + '\n')

            # for comment in comments:
            #     print(comment.text)

    def main(self):
        self.get_music_url()
        self.get_comments()
        print("下载完成！")
        self.browser.quit()


if __name__ == '__main__':
    singer = Taylor()
    with ThreadPoolExecutor(40) as t:
        t.submit(singer.main)
