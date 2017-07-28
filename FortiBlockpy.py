#!  /usr/bin/python
# -*- coding:utf-8 -*-


import getpass
import sys
from pexpect import pxssh
from FortiMail import mail_gonder
import time
from datetime import datetime


giris="""

            ****************************************************
               
                              FortiBlockpy
                     
                     Fortigate BLocked Traffic Alert System 
               
                           Faruk GÜNGÖR @2017 

            *****************************************************
"""


def login(ip,user,passw):
  try:
    session=pxssh.pxssh()
    session.force_password=True
    session.login(ip,user,passw,auto_prompt_reset=False)

    print ("Bilgiler yükleniyor. Bu işlem bir kaç saniye sürebilir ..")
    dosya = open("trafic_log.txt", "w")
    #session.sendline("execute log filter category 7")
    #session.prompt()
    #dosya.write(session.before)
    session.sendline("execute log filter device 2")#fortigate sets disk as logging device . if you use f.analyzer you should use this command (device 2 )
    session.prompt()
    dosya.write(session.before)
    session.sendline("execute log filter field policyid ??") # you should enter your policyid 
    session.prompt()
    dosya.write(session.before)
    session.sendline("execute log display ")
    session.prompt()

    dosya.write(session.before)
    dosya.flush()
    dosya.close()
    session.logout()
    session.close()
  except pxssh.ExceptionPexpect as e:
      print("login failed ")
      sys.exit()

#trafik loglarını okuyoruz
def log_oku():
    dosya=open("trafic_log.txt","r")
    a=0

    while(a==0):
        okunan=dosya.readline()
        strr=okunan.strip()
        if strr.startswith("1:"):
            global ilk_veri
            if ilk_veri.strip()!=strr:
                ilk_veri=strr

                print(" !!! Zararlı ip bloklarına [Yeni]erişim tespit edildi !!! ")
                indeks=strr.find("srcip")
                gonderilecek=ilk_veri[indeks:indeks+54]
                print(gonderilecek)
                print ("mail bekleniyor")
                ma=mail_gonder(" !!! Zararlı ip bloklarına [Yeni]erişim tespit edildi !!! " + gonderilecek)
                ma.mail()
                a=1


            else :
                print("Zararlı ip bloklarına [Yeni] trafik yok ")
                a=1

        elif strr=="0 logs found.":
          print(strr)
          a=1


print(giris)
ilk_veri="ilk veri"
cihaz_ip=raw_input("firewall ip :")
username=raw_input("username :")
parola=getpass.getpass("password :")
while(True):
   login(cihaz_ip,username,parola)
   log_oku()

   zaman=datetime.now()
   print(zaman)
   print("*"*50)
   time.sleep(60)
