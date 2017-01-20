#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
###############################
#                             #
#  (C) 2017 by Alex Mirtoff   #
#                             #
#  Записывает в MySQL таблицу #
#      оценки  абонентов      #
#     отдел сопровождения     #
#                             #
###############################
#

import sys
import MySQLdb
import re
import time

# input args
date = sys.argv[1]
callerid = sys.argv[2]
evaluation = sys.argv[3]
uid = sys.argv[4]
call_src = sys.argv[5]
rdnis = sys.argv[6]

operators_list = []

sip_interface_compile = re.compile('SIP/(\w*)-.+')
asterisk_database = MySQLdb.connect(host="localhost", user="***", passwd="***", db="***", charset='utf8')


def db_insert_evaluation(date, callerid, evaluation, uid, call_src, rdnis, asterisk_database):
	new_record = """INSERT INTO rating_os (date, callerid, evaluation, uid, call_src, rdnis)
	VALUES (%s, %s, %s, %s, %s, %s)"""
	add = asterisk_database.cursor()
	add.execute(new_record, (date, callerid, evaluation, uid, call_src, rdnis))

def db_get_cdr_by_uid(uid, asterisk_database):
	get_cdr_record = """SELECT dstchannel FROM cdr WHERE uniqueid=%s OR linkedid=%s"""
	get = asterisk_database.cursor()
	get.execute(get_cdr_record, (uid, uid))
	return get.fetchall()

def db_get_int_nums(list, asterisk_database):
	join_list = ', '.join(map(lambda x: '%s', list))
	get_int_nums_record = """SELECT number FROM softswitch WHERE intaccount IN (%s)""" % join_list
	get = asterisk_database.cursor()
	get.execute(get_int_nums_record, (list))
	tup = get.fetchall()
	tmp_lst = []
	for i in tup:
		tmp_lst.append(str(i[0]))
	return ','.join(tmp_lst)
	
def db_update_add_operator(extensions, uid, asterisk_database):
	update_record = """UPDATE rating_os SET operators = %s WHERE uid = %s"""
	upd = asterisk_database.cursor()
	upd.execute(update_record, (extensions, uid))
	
#	print "UID: %s" % uid
#	print "Список сотрудников которые говорили с абонентом: %s" % extensions
	
db_insert_evaluation(date, callerid, evaluation, uid, call_src, rdnis, asterisk_database)
time.sleep(10)
cdr_log = db_get_cdr_by_uid(uid, asterisk_database)

for index, item in enumerate(cdr_log):
	if item[0] is not None:
		operators_regexp = sip_interface_compile.findall(item[0])
		operators_list.append(operators_regexp[0])
db_update_add_operator(db_get_int_nums(list(set(operators_list)), asterisk_database), uid, asterisk_database)

