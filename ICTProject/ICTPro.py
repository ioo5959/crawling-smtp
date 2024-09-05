from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from itertools import chain

#크롬드라이버로 원하는 url로 접속
url = 'https://itc.pknu.ac.kr/html/03/01.php?category_idx=1'
driver = webdriver.Chrome() #크롬 드라이버 자동 다운로드 및 실행
driver.get(url) #크롬 드라이버에 url로 넣기
time.sleep(3) #실행되기까지의 시간으로 벌어줌


list_name = [] #이름 리스트
list_phone = [] #전화번호 리스트
list_email = [] #이메일 리스트
list_major = [] #전공 리스트

majors = driver.find_elements(By.XPATH, '//*[@id="container"]/div[2]/ul/li/a')
for i in majors:
    list_major.append(i.text)

for i in range(1,16):
    major_path = '//*[@id="container"]/div[2]/ul/li[{}]'.format(i)
    driver.find_element(By.XPATH, major_path).click() #탭 클릭
    time.sleep(2)

    lis1=[]
    lis2=[]
    lis3=[]


    # 데이터 수집
    names = driver.find_elements(By.XPATH, '//*[@id="container"]/div[2]/div/div/div[2]/div/div[1]/p')

    for i in names:
        lis1.append(i.text)
    list_name.append(lis1)

    phones = driver.find_elements(By.XPATH, '//*[@id="container"]/div[2]/div/div/div[2]/div/div[4]/div[2]')

    for i in phones:
        lis2.append(i.text)
    list_phone.append(lis2)

    emails = driver.find_elements(By.XPATH,'//*[@id="container"]/div[2]/div/div/div[2]/div/div[5]/div[2]')

    for i in emails:
        lis3.append(i.text)
    list_email.append(lis3)

#리스트를 해당 요소의 크기 만큼 늘리기
flat_list_major = [major for major, names in zip(list_major, list_name) for _ in names]
#이중 리스트 평탄화
flat_list_name = list(chain.from_iterable(list_name))
flat_list_phone = list(chain.from_iterable(list_phone))
flat_list_email = list(chain.from_iterable(list_email))

#zip 모듈을 이용해서 list 묶어주기
list_sum = list(zip(flat_list_major,flat_list_name,flat_list_phone,flat_list_email))

col = ['전공','이름','전화번호','이메일'] #컬럼명

df = pd.DataFrame(list_sum,columns=col) #pandas 데이터 프레임 형태로 가공

df.to_excel('정보융합대학.xlsx')

driver.quit()