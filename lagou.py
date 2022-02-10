from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

web = Chrome()

web.get("http://lagou.com")

# 找到某个元素， 点击它
el = web.find_element(By.XPATH, '/html/body/div[10]/div[1]/div[2]/div[2]/div[1]/div/p[1]/a')
el.click()  # 点击事件

time.sleep(1)  # 让浏览器缓一缓

# 找到输入框， 输入python => 输入回车/点击搜索按钮
web.find_element(By.XPATH, '/html/body/div[7]/div[1]/div[1]/div[1]/form/input[1]').send_keys('python', Keys.ENTER)

time.sleep(2)

# 查找存放数据的位置， 进行数据提取
# 找到页面中存放数据的所有的div
div_list = web.find_elements(By.XPATH, '//*[@id="jobList"]/div[1]/div')
for div in div_list:
    job_name = div.find_element(By.XPATH, './div[1]/div[1]/div[1]/a').text.split('[')[0]
    job_price = div.find_element(By.XPATH, './div[1]/div[1]/div[2]/span').text
    com_name = div.find_element(By.XPATH, './div[1]/div[2]/div[1]/a').text
    print('岗位名称：'+job_name, '薪酬：'+job_price, '公司名称：'+com_name, sep=' ')



