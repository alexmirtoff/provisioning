#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#############################
#                           #
# (C) 2016 by Alex Mirtoff  #
#                           #
# Абон отдел Невинка 100сек #
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
uid = sys.argv[3]

def send_email(date, in_num):

	fromaddr = "robot@asterisk.****.ru"
	toaddr = "ao.nevinka@******.net"
	admin = "mirtoff@******.net"
 
	msg = MIMEMultipart()
 
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Bcc'] = admin
	msg['Subject'] = "*** ASTERISK: Ожидание на линии более 100 секунд"
	msg['Date'] = formatdate(localtime = True)
	msg.set_charset("utf-8")
 
	body = '''Невинномысск, Абонентский отдел.
Абонент находился в ожидании ответа более 100 секунд:

-----------------------------------------------
 Время звонка    : %s
 Номер абонента  : %s
-----------------------------------------------
	
	''' % (date, in_num)
 
	msg.attach(MIMEText(body, 'plain', 'utf-8'))


	server = smtplib.SMTP('mail.********.net', 25)
	text = msg.as_string()
	recipients = [toaddr, admin]
	server.sendmail(fromaddr, recipients, text)
	server.quit()


time.sleep(100)

send_email(date, in_num)
exit()
