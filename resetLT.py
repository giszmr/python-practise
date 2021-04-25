#!/usr/bin/python2

import telnetlib
import os
import time

host153='10.9.65.153'
username='isadmin'
password='      '
finish='typ:isadmin>#'

#######################################
def do_login(tn):
    tn.read_until('login: ')
    tn.write(username + '\n')
    tn.read_until('password: ')
    tn.write(password + '\n')
    
    readinfo = tn.read_until(finish)
    if finish in readinfo:
        return 1
    else:
        return 0

########################################
def check_LT_status(tn, fd):
    tn.write("exit all\n")
    fd.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +  "show equipment slot lt:1/1/2 detail\n")
    tn.write("show equipment slot lt:1/1/2 detail\n")
    tn.write("exit all\n")
    time.sleep(1)

    readinfo = tn.read_very_eager()
    fd.write(readinfo)
    #time.sleep(180)
    if 'oper-status : enabled' in readinfo:
        return 1
    else:
        return 0

########################################
def lock_unlock_LT(tn, fd):
    fd.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start to lock LT\n')
    tn.write("exit all\n")
    tn.write("configure  equipment slot lt:1/1/2  no unlock\n")
    time.sleep(60)

    fd.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start to unlock LT\n')
    tn.write("exit all\n")
    tn.write("configure  equipment slot lt:1/1/2  unlock\n")
    tn.write("exit all\n")

    readinfo = tn.read_very_eager()
    fd.write(readinfo)
    if 'Error' in readinfo:
        return 0
    else:
        return 1

########################################
def lock_unlock_LT_test(tn, fd):
    lock_unlock_LT(tn, fd)
    while 1:
        if  check_LT_status(tn, fd) == 1:
            break
        time.sleep(4);
    fd.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'LT oper-status is enabled\n')


#########################################
if __name__ == '__main__':
    #telnet isam
    tn153=telnetlib.Telnet(host153)
    loginfo153 = do_login(tn153)
    if loginfo153 == 0:
        print 'login error'

    fd = open('./lockunlocklt.txt', 'a')

    for num in range(1, 10000):
        fd.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=============BEGIN "+str(num)+" BEGIN==============\n")
        #lock, unlock, check lt status
        lock_unlock_LT_test(tn153, fd)
        fd.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "=============ONGOING "+str(num)+" ONGOING==============\n")
        time.sleep(600)

    fd.close()
    tn153.close()

