from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib

baseUrl = 'https://www.google.com/search?q='
plusUrl = input('무엇을 검색할까요? : ')

url = baseUrl + quote_plus(plusUrl + " 등장인물")

driver = webdriver.Chrome("C:/Users/User/chromedriver_win32/chromedriver.exe")
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html)
list = []

sl = soup.select('.sATSHe')[0]
mk = sl.select('.JjtOHd')

for i in range(1, len(mk)):
    list.append(mk[i].string)
    
print(list)


driver.close()

