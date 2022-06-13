from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException, ElementNotInteractableException,NoSuchWindowException, NoSuchFrameException
import time

#네이버 들어가기
baseUrl = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query='
plusUrl = input('무엇을 검색할까요? : ')
#검색
url = baseUrl + quote_plus(plusUrl + " 등장인물")

driver = webdriver.Chrome("C:/Users/User/chromedriver_win32/chromedriver.exe")
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html)
list = []
try:
    #등장인물 찾기
    sl = soup.select('.title_box')
    #리스트에 저장
    for i in range(0, len(sl)):
        aTag = sl[i].find('a')
        list.append(aTag.string.split()[0])
    time.sleep(2)
    #기본정보 클릭
    driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div[1]/div[4]/div/div/ul/li[2]/a').send_keys(Keys.ENTER)
    html = driver.page_source
    soup = BeautifulSoup(html)
    #줄거리 가져오기
    sl = soup.select('.intro_box')[0].text.replace("'",'').replace('"','')
    sp = sl.split()
    #리스트에 추가
    for p in range(0, len(sp)):
        list.append(sp[p])
except:
        print("stop")
#print(list)
driver.close()
