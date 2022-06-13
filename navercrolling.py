from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException, ElementNotInteractableException,NoSuchWindowException, NoSuchFrameException
import time

baseUrl = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query='
plusUrl = input('무엇을 검색할까요? : ')

url = baseUrl + quote_plus(plusUrl + " 등장인물")

driver = webdriver.Chrome("C:/Users/User/chromedriver_win32/chromedriver.exe")
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html)
list = []

sl = soup.select('.title_box')

for i in range(0, len(sl)):
    aTag = sl[i].find('a')
    list.append(aTag.string.split()[0])

time.sleep(2)

driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div[1]/div[4]/div/div/ul/li[2]/a').send_keys(Keys.ENTER)

html = driver.page_source
soup = BeautifulSoup(html)

sl = soup.select('.intro_box')[0].text.replace("'",'').replace('"','')
sp = sl.split()
for p in range(0, len(sp)):
        list.append(sp[p])

driver.close()
