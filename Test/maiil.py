#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 导入所需模块
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 邮箱帐号和授权码，连接和登录邮箱
mailUser = "26125482@qq.com"
mailPass = "orjdxktornhobhba"
smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
smtpObj.login(mailUser, mailPass)

#我们的邮箱是yequbiancheng@baicizhan.com，我们希望你的邮件标题是“给夜曲编程的一封信——xxx”，xxx是你的昵称或者姓名。


# 发件人、收件人
sender = "26125482@qq.com"
# receiverDict = {"xixi": "adc@yequ.com", "kiki": "def@yequ.com", "tongtong": "yza@yequ.com"}
receiver = 'yequbiancheng@baicizhan.com'
# 文件路径
# path = "/Users/aLing"

message = MIMEMultipart()
message["From"] = Header(f"huangyt<{sender}>")
message["To"] = Header(f"夜曲<{receiver}>")
message["Subject"] = Header(f"给夜曲编程的一封信——huangyt")
mailContent = MIMEText(f"Dear 夜曲编程的同事：非常感谢这次学习的经历，期待你们的菜单", "plain", "utf-8")
message.attach(mailContent)
smtpObj.sendmail(sender, receiver, message.as_string())
print("发送成功")

'''
for receiver in receiverDict:
    # 编辑并整合发件人、收件人、主题信息
    message = MIMEMultipart()
    message["From"] = Header(f"阿玲<{sender}>")
    message["To"] = Header(f"{receiver}<{receiverDict[receiver]}>")
    message["Subject"] = Header(f"{receiver}yequbiancheng@baicizhan.com")

    # 编辑邮件正文
    mailContent = MIMEText(f"Dear {receiver} 邀请你参加年会", "plain", "utf-8")

    # 读取图片文件
    filePath = path + "/" + receiver + ".jpg"
    with open(filePath, "rb") as imageFile:
        fileContent = imageFile.read()

    # 编辑附件信息
    att = MIMEImage(fileContent)
    att.add_header("Content-Disposition", "attachment", filename="邀请函.jpg")

    # 整合正文和图片
    message.attach(mailContent)
    message.attach(att)
'''
    # 发送邮件
    # smtpObj.sendmail(sender, receiverDict[receiver], message.as_string()) print("发送成功")
