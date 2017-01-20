#!/usr/bin/python
#-*- coding: utf-8 -*-
#
############################
#                          #
# (C) 2016 by Alex Mirtoff #
#                          #
#      Reboot phone        #
#                          #
############################
#

import sys
import subprocess
import shlex

peer_ip = sys.argv[1]

curl_str = "curl --digest -u admin:*** http://"+peer_ip+"/admin/reboot"
args = shlex.split(curl_str)
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
result = p.communicate()[0]

