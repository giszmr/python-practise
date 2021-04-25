#!/usr/bin/python
#coding=utf-8

def func():
  print "module employee"

class Employee:
  'Basic class.'
  empCount = 0

  def __init__(self, name, salary):
    self.name   = name
    self.salary = salary
    Employee.empCount +=1

  def displayCount(self):
    print "Total Employee %d" % self.empCount

  def displayEmployee(self):
    print "Name: ", self.name, "salary: ", self.salary

