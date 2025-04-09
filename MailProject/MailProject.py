import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
import os

def send_email(sender_email, receiver_email, app_password, subject, text, html, attachs):
    try:
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
        for fname in os.listdir(attachs):
            file_name = os.path.join(attachs,fname) # 첨부파일명
            with open(file_name, 'rb') as attach_file:
                attachment = MIMEApplication(attach_file.read())
                attachment.add_header('Content-Disposition', 'attachment', filename=fname)
            message.attach(attachment)

        # 이메일 서버 이용
        with smtplib.SMTP_SSL("zmsmtp.mailplug.com", 465) as server:
            server.login(sender_email, app_password)  # 로그인
            print("로그인 성공!")
            # sendmail 함수를 이용하여 메일 보내기
            server.sendmail(sender_email, receiver_email, message.as_string())

        return True # 전송 성공

    except smtplib.SMTPAuthenticationError:
        print("로그인 실패: 아이디/비밀번호가 올바른지 확인하세요.")
    except smtplib.SMTPServerDisconnected:
        print("서버 연결 끊김: SMTP 서버 설정이 올바른지 확인하세요.")
    except Exception as e:
        print(f"오류 발생: {e}")

    return False # 전송 실패





if __name__ == "__main__": #main함수

    count = 0
    paramsExcel = pd.read_excel('./params.xlsx')
    print(paramsExcel)

    params = {} #보내는 사람, 비밀번호, 받는 사람, 보낼 내용, 첨부파일..
    for line in paramsExcel.values:
        key, value = line[:2]
        params[key] = value

    sender_email = params['sender_email']
    app_password = params['app_password']
    receiver_file = params['receiver_email_list']
    content_file = params['contentfile_name']
    attachs = params['attachfile_folder']

    print('-------------')
    print('loaded Parameters')
    print(params)
    print('------------------')

    f = open(content_file, 'r', encoding='utf-8')  # 이메일 내용이 있는 텍스트 파일 열기
    subject = f.readline() #맨 처음 한 줄 제목
    text = f.read()
    f.close()

    html = f"<html><body><p>{text.replace('\n', '<br>')}</p></body></html>"  # html형식으로 본문 만들기

    email_lis = pd.read_excel(receiver_file, usecols=["이메일"]) #메일 주소가 있는 엑셀 파일 접근
    for index, row in email_lis.iterrows(): #한 행씩 접근
        receiver_email = str(row["이메일"])
        success = send_email(sender_email, receiver_email, app_password, subject, text, html, attachs)
        if success:
            print("전송완료")
            count = count + 1
        else:
            print("전송실패")

    print(count)