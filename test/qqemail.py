import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import zipfile
import os

auth_code = 'tpgmgswayrxqebji'
sender = "2267592072@qq.com"
receiver = ["zhouji0726@163.com"]  # 可写多个
smtp_server = "smtp.qq.com"
smtp_port = 465

def zip_report():
    if not os.path.isdir("files"):
        os.mkdir("files")
    zip_path = "files/allure-report.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("allure-report"):
            for file in files:
                path = os.path.join(root, file)
                arcname = os.path.relpath(path, "allure-report")
                zipf.write(path, arcname)
    return zip_path

def send_email_with_qq(zip_file):
    # 构建邮件内容
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(receiver)
    msg['Subject'] = "自动化测试报告 - Allure"

    body = MIMEText("Hi，测试已完成，报告见附件", 'plain', 'utf-8')
    msg.attach(body)

    with open(zip_file, 'rb') as f:
        report = MIMEApplication(f.read())
        report.add_header('Content-Disposition', 'attachment', filename='allure-report.zip')
        msg.attach(report)

    # 发送邮件
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender, auth_code)
        server.send_message(msg)
        server.quit()
    # print("✅ 邮件已发送！")
    print("邮件已发送！")