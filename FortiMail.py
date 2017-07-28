#! /usr/bin/ python
# -*- coding:utf-8 -*-


import smtplib

class mail_gonder():

    def __init__(self,mesaj):
        self.mesaj=mesaj


    def mail(self):

        gonderen = "sender e-mail"
        pswd = "sender e-mail passwd"
        alici = "receiver e mail "
        cc = "if you need add cc e-mail "
        body=self.mesaj
        print(self.mesaj)
        try:
            server = smtplib.SMTP("smtp.live.com", 587)
            server.starttls()
            server.login(gonderen, pswd)
            server.sendmail(gonderen,[alici,cc],body)
            server.close()
            print("mail gönderildi")
        except smtplib.SMTPException as e:
            print(str(e))




