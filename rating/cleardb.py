#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#############################
#                           #
# (C) 2016 by Alex Mirtoff  #
#                           #
#  Очистка внутренней БД    #
#     Asterisk по cron      #
#                           #
#############################
#

import subprocess
import re 

show_calls_cmd = subprocess.Popen('/usr/sbin/asterisk -rx "core show calls"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
calls = show_calls_cmd.stdout.read()
calls_regexp = re.findall('^(\d{1,2}) active call.*', calls)

if calls_regexp[0] == '0':
	clear_db_cmd = subprocess.Popen('/usr/sbin/asterisk -rx "database deltree getnum"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
