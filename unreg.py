#!/usr/bin/python
#-*- coding: utf-8 -*-
#
############################
#                          #
# (C) 2016 by Alex Mirtoff #
#                          #
#  Разрегистрирует аппарат #
#                          #
############################
#

import xml.etree.ElementTree as ET
import re, os, sys
import shutil
import subprocess
import shlex
import datetime
import time

peer_ip = sys.argv[1]
peer_num = sys.argv[2]

pswd = "****"
proxy = "10.20.253.11"

if peer_num == '211':
    username = "androsova_unreg"
if peer_num == '212':
    username = "beginina_unreg"
if peer_num == '213':
    username = "borodina_unreg"
if peer_num == '214':
    username = "lysenko_unreg"
if peer_num == '270':
    username = "namgirova_unreg"
if peer_num == '281':
    username = "ryabinina_unreg"
if peer_num == '290':
    username = "sazonova_unreg"
if peer_num == '291':
    username = "fedortsova_unreg"
if peer_num == '376':
    username = "mirtest_unreg"

ipre = re.findall('(\d*).(\d*).(\d*).(\d*)', peer_ip)


default_phone_xml = "/home/provisioning/phone-xml/default.xml"
tmp_dir = "/home/provisioning/temp/"
tmp_filename = peer_num+"_"+ipre[0][0]+"-"+ipre[0][1]+"-"+ipre[0][2]+"-"+ipre[0][3]+".xml"
full_tmp = tmp_dir+tmp_filename
www_path = "/var/www/provisioning/"
full_www = www_path+tmp_filename
shutil.copyfile(default_phone_xml, full_tmp)

phone_config_tree = ET.parse(full_tmp)
phone_config_root = phone_config_tree.getroot()

for phone_item in phone_config_root.getiterator():
    if phone_item.tag == 'Display_Name_1_':
        phone_item.text = "NO REGISTRATION"
    if phone_item.tag == 'User_ID_1_':
        phone_item.text = username
    if phone_item.tag == 'Password_1_':
        phone_item.text = pswd
    if phone_item.tag == 'Auth_ID_1_':
        phone_item.text = username
    if phone_item.tag == 'Station_Name':
        phone_item.text = "NO REGISTRATION"
    
phone_config_tree.write(full_tmp)

shutil.copyfile(full_tmp, full_www)
os.unlink(full_tmp)

curl_str = "/usr/bin/curl --digest -u admin:****** http://"+peer_ip+"/admin/resync?http://10.*.*.*/provisioning/"+tmp_filename
args = shlex.split(curl_str)
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
result = p.communicate()[0]

current_date = datetime.datetime.now().strftime("%d-%m-%Y")
current_time = datetime.datetime.now().strftime("%H:%M:%S")
log_file = "/home/provisioning/log/"+current_date+".log"
log_str = current_date+" "+current_time+" | --- Unregistration OK | IP: "+peer_ip+", Phone number: "+peer_num+", Username: "+username+"\n"
with open(log_file, "a") as my_log_file:
    my_log_file.write(log_str)
my_log_file.close()

time.sleep(10)
os.unlink(full_www)
