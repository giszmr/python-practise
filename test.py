#!/usr/bin/python2

import os
import thread
import threading
import time
import itertools #import permutations

def string_test():
    print "**********string test************"
    str = 'hello world'
    str1 = 'ooooo'
    print type(str)
    print str[:8]
    print str[0:8]
    print str[2:]
    print str[2:10]
    print str[3:-1]
    print str[3:-1] * 3
    print str[-3:-1]
    print str[1:20]
    print str[:]

def list_test():
    print "**********list test************"
    list = [ 'runoob', 786 , 2.23, 'john', 70.2 ]
    tinylist = [123, 'john']
    print type(list)
    print list               # 
    print list[0]            # 
    print list[1:3]          #  
    print list[2:]           #
    list[2] = 1000
    print tinylist * 2       # 
    print list + tinylist    #

def tuple_test():
    print "**********tuple test************"
    tuple = ( 'runoob', 786 , 2.23, 'john', 70.2 )
    tinytuple = (123, 'john')
    print type(tuple)
    print tuple               #
    print tuple[0]            # 
    print tuple[1:3]          #  
    print tuple[2:]           #
    print tuple[:3]
    #tuple[2] = 1000          # could not be modified
    print tinytuple * 2       # 
    print tuple + tinytuple   #

def dictionary_test():
    print "**********dictionary test************"
    dict = {}
    dict['one'] = "This is one"
    dict[2] = "This is two"
    tinydict = {'name': 'john','code':6734, 'dept': 'sales'}
    print type(tinydict)
    print dict['one']          # 
    print dict[2]              # 
    print tinydict             # 
    print tinydict.keys()      # 
    print tinydict.values()    #

money = 1
def globalVal_test():
    global money            #if this line is deleted, the next line will goes wrong.
    money = money + 1
    print money

def function_test():
    print locals()   #return all names that can be accessed in this place. return dictionary.
    print '****************'
    print globals()  #return all global names that can be accessed in this place. return dictionary.

def input_test():
    str = raw_input("Please input: ")
    print "Your input is " + str
    str1 = input("Please input: ")
    print "Your input is ", str1

def iter_test():
#    for i in permutations("1234", 3)
#        print i
  pass

def printtime(threadname, delay):
  count = 0
  while count < 5:
    count += 1
    time.sleep(delay)
    print "%s: %s" % ( threadname, time.ctime(time.time()) )

def thread_test():
  try:
    thread.start_new_thread( printtime, ("thread 1", 2) )
    thread.start_new_thread( printtime, ("thread 2", 4) )
  except:
    print "Error: Unable to start thread"
  time.sleep(40)

if __name__ == '__main__':
    tuple_test()



 

