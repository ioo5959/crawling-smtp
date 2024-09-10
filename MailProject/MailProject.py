import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd


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

    #이메일 서버 이용
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password) #로그인
        #sendmail 함수를 이용하여 메일 보내기
        server.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == "__main__": #main함수

    sender_email = "gomath72@gmail.com"
    app_password = "iqny kqsm cukz prfj" #앱비밀번호

    f = open('emailcontent.txt', 'r')  # 파일 열기
    subject = f.readline() #맨 처음 한 줄 제목
    text = f.read()
    f.close()

    html = f"<html><body><p>{text.replace('\n', '<br>')}</p></body></html>"  # html형식으로 본문 만들기

    email_lis = pd.read_excel('test.xlsx', usecols=["이메일"])
    for index, row in email_lis.iterrows(): #한 행씩 접근
        receiver_email = row["이메일"]
        send_email(sender_email, receiver_email, app_password, subject, text, html)




