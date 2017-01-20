#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
###############################
#                             #
#  (C) 2016 by Alex Mirtoff   #
#                             #
#  Записывает в MySQL таблицу #
#      оценки  абонентов      #
#                             #
###############################
#

import sys
import MySQLdb

callerid = sys.argv[1]
operator = sys.argv[2]
uid = sys.argv[3]
call_date = sys.argv[4]
evaluation = sys.argv[5]
queuename = sys.argv[6]

	

new_record = """INSERT INTO rating_support (date, callerid, exten, queue, evaluation, uid)
                VALUES (%s, %s, %s, %s, %s, %s)"""

db = MySQLdb.connect(host="localhost", user="***", passwd="***", db="***", charset='utf8')
add = db.cursor()

add.execute(new_record, (call_date, callerid, operator, queuename, evaluation, uid))

db.close()

