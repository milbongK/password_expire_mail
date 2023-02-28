# -*- coding: utf-8 -*-
# 한글 사용할 수 있도록 허용

import os
import subprocess
from datetime import datetime
import smtplib
from email.mime.text import MIMEText


#************
# full_usr_info -> export in /etc/passwd all data
# full_usr_id -> export in /etc/passwd used the /bin/bash ID
# full_usr_email -> export in /etc/passwd send mail address
# TODAY -> today
# LINUX_START_DAY -> need for calculation to usr passwd expire day
# until_change_passwd -> find passwd expire day
# max_use_passwd -> use the passwd Maxium
full_usr_info = []
full_usr_id_list = []
full_usr_email_list = []
shadow_usr_expire_info = []
shadow_usr_expire_day_list = []
shadow_usr_id_list = []
shadow_usr_max_passwd_list = []
TODAY = datetime.now()
LINUX_START_DAY = datetime(1970,1,1)
until_change_passwd = 0
max_use_passwd = 0

# call /etc/shadow files info
linux_shadow_usr = subprocess.check_output(['cat', '/etc/shadow'])
linux_shadow_usr_list = linux_shadow_usr.split("\n")
linux_shadow_usr_list.remove('')

# call /etc/passwd files info
linux_passwd_usr = subprocess.check_output(['cat', '/etc/passwd'])
linux_passwd_usr_list = linux_passwd_usr.split("\n")
linux_passwd_usr_list.remove('')

# call /etc/hostname files info
machine_name = subprocess.check_output(['cat', '/etc/hostname'])

#find usr list, email list, passwd expire day list
def find_usr_list():
    global linux_passwd_usr_list, full_usr_info, full_usr_id_list, full_usr_email_list, linux_shadow_usr_list, shadow__usr_expire_info, shadow_usr_id_list, shadow_usr_expire_day_list, shadow_usr_max_passwd_list
    i = 0
    while i < len(linux_passwd_usr_list):
        find_text_in_usr = linux_passwd_usr_list[i]
        find_text_in_shadow = linux_shadow_usr_list[i]

        if find_text_in_usr.find("/bin/bash") != -1:

            # split the /etc/passwd in use "/bin/bash", /etc/shadow all daya
            full_usr_info = find_text_in_usr.split(":")
            shadow_usr_info = find_text_in_shadow.split(":")


            # /etc/passwd find id list, /etc/shadow find id list
            full_usr_id = full_usr_info[0]
            full_usr_id_list.append(full_usr_id)
            shadow_usr_id = shadow_usr_info[0]
            shadow_usr_id_list.append(shadow_usr_id)

            # /etc/shadow find passwd expire day
            shadow_usr_expire_day = shadow_usr_info[2]
            shadow_usr_expire_day_list.append(shadow_usr_expire_day)
            shadow_usr_max_passwd = shadow_usr_info[4]
            shadow_usr_max_passwd_list.append(shadow_usr_max_passwd)

            # find email list
            full_usr_email = full_usr_info[4]
            full_usr_email_list.append(full_usr_email)
        i += 1
    return 0



# change passwd day
def expire_id_send_mail():
    global until_change_passwd, to_address, from_address, machine_name
    i = 0
    while i < len(shadow_usr_id_list):
        if shadow_usr_expire_day_list[i] != '':
            #print(until_passwd_change_day)
            expire_day = shadow_usr_expire_day_list[i]
            passwd_max_day = shadow_usr_max_passwd_list[i]
            to_day = (TODAY - LINUX_START_DAY).days
            until_change_passwd = (int(expire_day) + int(passwd_max_day)) - to_day
            ## 남은 만료일이 해당 숫자보다 적을 시, 메일 발송
            if until_change_passwd <= 7:
                #send mail function ----------------------------------
                from_address = "admin@test.com"
                to_address = full_usr_email_list[i] #/etc/passwd 3th
                msg1="------------------------------------\n"\
                "서버명: {0}\n"\
                "암호 사용 만료 안내\n"\
                "------------------------------------\n\n"\
                "안녕하세요.\n\n"\
                "계정 [{1}]의 암호 만료일이 [{2}]일 남았습니다.\n"\
                "[{2}]일 안으로 암호를 변경해 주세요.\n\n"\
                "**암호 만료일을 지나도 계정이 잠기지 않습니다.".format(machine_name, shadow_usr_id_list[i], until_change_passwd)
                s = smtplib.SMTP('smtp.test.com', 25)
                msg = MIMEText(msg1)
                msg['Subject'] = "서버 계정 암호 만료 안내 - {0}".format(machine_name)
                s.sendmail(from_address, to_address, msg.as_string())
                print(shadow_usr_id_list[i])
                print("send maill succ")
        i += 1
    return 0

#------------------------------------------------------------------------------------------------------------------

find_usr_list()
expire_id_send_mail()
