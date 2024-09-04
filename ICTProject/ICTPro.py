from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#크롬드라이버로 원하는 url로 접속
url = 'https://itc.pknu.ac.kr/html/03/01.php?category_idx=1'
driver = webdriver.Chrome() #크롬 드라이버 자동 다운로드 및 실행
driver.get(url) #크롬 드라이버에 url로 넣기
time.sleep(3) #실행되기까지의 시간으로 벌어줌

#탭 클릭
#driver.find_element(By.XPATH, '//*[@id="container"]/div[2]/ul/li[1]/a').click()
#time.sleep(2)

list_name = [] #이름 리스트
list_phone = [] #전화번호 리스트
list_email = [] #이메일 리스트

#데이터 수집
names = driver.find_elements(By.CSS_SELECTOR, ".fs20.fwb")
#클래스명이 두 개이기 때문에 CSS_SELECTOR를 이용해서 요소를 가져와야 함

for i in names:
    list_name.append(i.text)


phones = driver.find_elements(By.CSS_SELECTOR, ".fl.mmgb_5")

for i in phones:
    list_phone.append(i.text)


print(list_name)
print(list_phone)