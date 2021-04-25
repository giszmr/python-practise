#!/usr/bin/python2

import telnetlib
import os
import time

host88='10.9.65.88'
host87='10.9.68.87'
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
def create_pg(tn, nodename, type, loop):
    print '**********' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start to create pg ' + str(loop) + '**************'
    tn.write("exit all\n")
    print "configure dual-parenting protection-group pon:1/1/3/"+ str(loop) +" prot-type "+type+" peer-node-name "+ nodename +" protection-group-id " + str(loop)
    tn.write("configure dual-parenting protection-group pon:1/1/3/"+ str(loop) +" prot-type "+type+" peer-node-name "+ nodename +" protection-group-id " + str(loop) + "\n")
    #time.sleep(5)
    #print "configure dual-parenting protection-group pon:1/1/3/"+ str(loop) +" enabled"
    #tn.write("configure dual-parenting protection-group pon:1/1/3/"+ str(loop) +" enabled\n")
    #time.sleep(5)
    tn.write("exit all\n")
    #time.sleep(0.05) 
    readinfo = tn.read_very_eager()
    print readinfo
    #time.sleep(180)
    if 'Error' in readinfo:
        return 0
    else:
        return 1

########################################
def enable_pg(tn, nodename, type, loop):
    print '**********' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start to create pg ' + str(loop) + '**************'
    tn.write("exit all\n")
    #print "configure dual-parenting protection-group pon:1/1/3/"+ str(loop) +" prot-type "+type+" peer-node-name "+ nodename +" protection-group-id " + str(loop)
    #tn.write("configure dual-parenting protection-group pon:1/1/3/"+ str(loop) +" prot-type "+type+" peer-node-name "+ nodename +" protection-group-id " + str(loop) + "\n")
    #time.sleep(5)
    print "configure dual-parenting protection-group pon:1/1/3/"+ str(loop) +" enabled"
    tn.write("configure dual-parenting protection-group pon:1/1/3/"+ str(loop) +" enabled\n")
    #time.sleep(5)
    tn.write("exit all\n")
    #time.sleep(0.05) 
    readinfo = tn.read_very_eager()
    print readinfo
    #time.sleep(180)
    if 'Error' in readinfo:
        return 0
    else:
        return 1

########################################
def create_enable_pgs(tn87, tn88):
    for num in range(1,17):
        createinfo87 = create_pg(tn87, "a", "primary", num)
        enable_pg(tn87, "a", "primary", num)
        createinfo88 = create_pg(tn88, "b", "secondary", num)
        enable_pg(tn88, "b", "secondary", num)
        time.sleep(0.05)
        if createinfo87 == 0 or createinfo88 == 0:
            print 'there is an alarm after creating pg. stop here!'

########################################
def delete_pg(tn, loop):
    print '*************' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start delete pg ' + str(loop) +'***************'
    tn.write("exit all\n")
    print "configure dual-parenting protection-group pon:1/1/3/" + str(loop) + " no enabled"
    tn.write("configure dual-parenting protection-group pon:1/1/3/" + str(loop) + " no enabled\n")
    print "configure dual-parenting no protection-group pon:1/1/3/" + str(loop)
    tn.write("configure dual-parenting no protection-group pon:1/1/3/" + str(loop) + "\n\n")
    tn.write("exit all\n")
    readinfo = tn.read_very_eager()
    print readinfo
    if 'Error' in readinfo:
        return 0
    else:
        return 1

########################################
def delete_pgs(tn87, tn88):
    for num in range(1,17):
        deleteinfo87 = delete_pg(tn87, num)
        deleteinfo88 = delete_pg(tn88, num)
        time.sleep(0.05)
        if deleteinfo87 == 0 or deleteinfo88 == 0:
            print 'there is an alarm after deleting pg. stop here!'

#########################################
if __name__ == '__main__':
    #telnet isam
    tn87=telnetlib.Telnet(host87)
    tn88=telnetlib.Telnet(host88)
    loginfo87 = do_login(tn87)
    loginfo88 = do_login(tn88)
    if loginfo87 == 0 or loginfo88 == 0:
        print 'login error'

    for num in range(1, 11):
        print("=============BEGIN "+str(num)+" BEGIN==============")
        #create and enable all pgs
        create_enable_pgs(tn87, tn88)
        print("=============ONGOING "+str(num)+" ONGOING==============")
        time.sleep(240)
        #delete all pgs
        delete_pgs(tn87, tn88)
        print("=============END "+str(num)+" END==============")
        time.sleep(240)

    tn87.close()
    tn88.close()

