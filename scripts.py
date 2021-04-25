#!/usr/bin/python2

import telnetlib
import os
import time

host='10.9.65.152'
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
def create_pg(tn):
    print '**********' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start to create pg**************'
    tn.write("""configure port-protection chpair:1/1/1/1 paired-port chpair:1/1/2/1\n
configure port-protection chpair:1/1/1/2 paired-port chpair:1/1/2/2\n
configure port-protection chpair:1/1/1/3 paired-port chpair:1/1/2/3\n
configure port-protection chpair:1/1/1/4 paired-port chpair:1/1/2/4\n
configure port-protection chpair:1/1/1/5 paired-port chpair:1/1/2/5\n
configure port-protection chpair:1/1/1/6 paired-port chpair:1/1/2/6\n
configure port-protection chpair:1/1/1/7 paired-port chpair:1/1/2/7\n
configure port-protection chpair:1/1/1/8 paired-port chpair:1/1/2/8\n
configure port-protection chpair:1/1/3/1 paired-port chpair:1/1/4/1\n
configure port-protection chpair:1/1/3/2 paired-port chpair:1/1/4/2\n
configure port-protection chpair:1/1/3/3 paired-port chpair:1/1/4/3\n
configure port-protection chpair:1/1/3/4 paired-port chpair:1/1/4/4\n
configure port-protection chpair:1/1/3/5 paired-port chpair:1/1/4/5\n
configure port-protection chpair:1/1/3/6 paired-port chpair:1/1/4/6\n
configure port-protection chpair:1/1/3/7 paired-port chpair:1/1/4/7\n
configure port-protection chpair:1/1/3/8 paired-port chpair:1/1/4/8\n
configure port-protection chpair:1/1/5/1 paired-port chpair:1/1/6/1\n
configure port-protection chpair:1/1/5/2 paired-port chpair:1/1/6/2\n
configure port-protection chpair:1/1/5/3 paired-port chpair:1/1/6/3\n
configure port-protection chpair:1/1/5/4 paired-port chpair:1/1/6/4\n
configure port-protection chpair:1/1/5/5 paired-port chpair:1/1/6/5\n
configure port-protection chpair:1/1/5/6 paired-port chpair:1/1/6/6\n
configure port-protection chpair:1/1/5/7 paired-port chpair:1/1/6/7\n
configure port-protection chpair:1/1/5/8 paired-port chpair:1/1/6/8\n
configure port-protection chpair:1/1/7/1 paired-port chpair:1/1/11/1\n
configure port-protection chpair:1/1/7/2 paired-port chpair:1/1/11/2\n
configure port-protection chpair:1/1/7/3 paired-port chpair:1/1/11/3\n
configure port-protection chpair:1/1/7/4 paired-port chpair:1/1/11/4\n
configure port-protection chpair:1/1/7/5 paired-port chpair:1/1/11/5\n
configure port-protection chpair:1/1/7/6 paired-port chpair:1/1/11/6\n
configure port-protection chpair:1/1/7/7 paired-port chpair:1/1/11/7\n
configure port-protection chpair:1/1/7/8 paired-port chpair:1/1/11/8\n
exit all\n""")
    time.sleep(10) 
    readinfo = tn.read_very_eager()
    print readinfo
    time.sleep(180)
    if 'Error' in readinfo:
        return 0
    else:
        return 1
    

########################################
def delete_pg(tn):
    print '*************' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start delete pg***************'
    tn.write("""configure no port-protection chpair:1/1/1/[1...8]\n
configure no port-protection chpair:1/1/3/[1...8]\n
configure no port-protection chpair:1/1/5/[1...8]\n
configure no port-protection chpair:1/1/7/[1...8]\n
exit all\n""")
    time.sleep(60) 
    readinfo = tn.read_very_eager()
    print readinfo
    if 'Error' in readinfo:
        return 0
    else:
        return 1

def switchover(tn):
    print '*************' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start switchover*************'
    tn.write("""admin port-protection chpair:1/1/7/4 activate no-interface\n
exit all\n""")
    time.sleep(180)
    readinfo = tn.read_very_eager()
    print readinfo
    if 'Error' in readinfo:
        return 0
    else: 
        return 1

def admincp(tn, strState):
    print '*************' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start admin ' + strState
    tn.write("configure channel-pair interface 1/1/7/4 admin-state " + strState + "\n")
    tn.write("configure channel-pair interface 1/1/11/4 admin-state " + strState + "\n")
    time.sleep(180)
    readinfo = tn.read_very_eager()
    print readinfo
    if 'Error' in readinfo:
        return 0
    else:
        return 1


#########################################
if __name__ == '__main__':
    #telnet isam
    tn=telnetlib.Telnet(host)
    loginfo = do_login(tn)
    if loginfo == 0:
        print 'login error'
    for num in range(1,500):
        print num
        #delete PG
        deleteinfo = delete_pg(tn)
        if deleteinfo == 0:
            print 'there is an alarm after deleting pg. stop here!'
            break
        #create PG
        createinfo = create_pg(tn)
        if createinfo == 0:
            print 'there is an alarm after creating pg. stop here!'
            break
        #admin up cp4
        admincp(tn, 'up')
        #switchover 3 times
        for i in range(1,4):
            switchinfo = switchover(tn)
            if switchinfo == 0:
                print 'there is an alarm after switchover. stop here!'
                break
        #admin down cp4
        admincp(tn, 'down')
    tn.close()
