#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#############################
#                           #
# (C) 2016 by Alex Mirtoff  #
#                           #
# Рассылка оценок на почту  #
#                           #
#############################
#

import smtplib
import sys
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from email.Utils import formatdate
 
date = sys.argv[1]
in_num = sys.argv[2]
op_num = int(sys.argv[3])
queue = sys.argv[4]
evaluation = int(sys.argv[5])
uid = sys.argv[6]

def num_to_names(op_num):
    switcher = {
	358: "* Михаил",
	258: "* Андрей",
	350: "* Николай",
	351: "* Михаил",
	352: "* Михаил",
	353: "* Константин",
	354: "* Евгений",
	356: "* Александр",
	357: "* Андрей",
	373: "* Илья",
	372: "* Владимир",
	359: "* Сергей",
	360: "* Илья",
	361: "* Александр",
	362: "* Роман",
	363: "* Захар",
	364: "* Максим",
	365: "* Алексей",
	366: "* Сергей",
	368: "* Антон",
	369: "* Владимир",
	374: "* Михаил",
	370: "* Максим",
	377: "* Алексей",
	375: "* Илья",
    }
    return switcher.get(op_num, "---null---")

op_name = num_to_names(op_num)

if evaluation > 2:
    exit()

time.sleep(15)

fromaddr = "robot@asterisk.*****.ru"
toaddr = "tech@*****.net"
 
msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "*** ASTERISK: Система оценки операторов"
msg['Date'] = formatdate(localtime = True)
msg.set_charset("utf-8")
 
body = '''Что-то пошло не так и вам поставили плохую оценку :(
          
-----------------------------------------------
 Время звонка    : %s
 Номер абонента  : %s
 Номер оператора : %s
 Имя оператора   : %s
 Оценка          : %s
 Очередь         : %s
-----------------------------------------------

Файл с записью разговора прикреплен к сообщению.
''' % (date, in_num, op_num, op_name, evaluation, queue)
 
msg.attach(MIMEText(body, 'plain', 'utf-8'))


attach_name = uid+'.mp3'
filename = '/var/spool/asterisk/monitor/'+ uid +'.wav.mp3'
attachment = open(filename, "rb")
 
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % attach_name)
 
msg.attach(part)
 
server = smtplib.SMTP('mail.*****.net', 25)
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
