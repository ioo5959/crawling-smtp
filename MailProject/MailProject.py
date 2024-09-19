import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
import sys
import os

def send_email(sender_email, receiver_email, app_password, subject, text, html):
    #이메일 구성
    message = MIMEMultipart("alternative")
    message["Subject"] = subject #제목
    message["From"] = sender_email #보내는 사람
    message["To"] = receiver_email #받는 사람

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    #첨부파일
    for i in range(5, len(sys.argv)):
        fname = sys.argv[i]
        print(os.path.exists(fname))
        file_name = fname # 첨부파일명
        with open(file_name, 'rb') as attach_file:
            attachment = MIMEApplication(attach_file.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=fname)
        message.attach(attachment)

    #이메일 서버 이용
    with smtplib.SMTP_SSL("zmsmtp.mailplug.com", 465) as server:
        server.login(sender_email, app_password) #로그인
        #sendmail 함수를 이용하여 메일 보내기
        server.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == "__main__": #main함수


    sender_email = sys.argv[1]
    app_password = sys.argv[2]
    receiver_file = sys.argv[3]
    content_file = sys.argv[4]


    f = open(content_file, 'r', encoding='utf-8')  # 이메일 내용이 있는 텍스트 파일 열기
    subject = f.readline() #맨 처음 한 줄 제목
    text = f.read()
    f.close()

    html = f"<html><body><p>{text.replace('\n', '<br>')}</p></body></html>"  # html형식으로 본문 만들기

    email_lis = pd.read_excel(receiver_file, usecols=["이메일"]) #메일 주소가 있는 엑셀 파일 접근
    for index, row in email_lis.iterrows(): #한 행씩 접근
        receiver_email = row["이메일"]
        send_email(sender_email, receiver_email, app_password, subject, text, html)
        print("전송완료")




