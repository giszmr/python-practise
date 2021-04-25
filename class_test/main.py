#!/usr/bin/python
#coding=utf-8

#from company import employee
#import company.employee
from company import *

if __name__ == '__main__':
  employee.func()
  someGuy = employee.Employee("zmr", 100)
  someGuy1 = employee.Employee("lvcc", 1000)
  someGuy.displayCount()
  someGuy.displayEmployee()
  someGuy1.displayEmployee()

