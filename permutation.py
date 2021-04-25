#!/usr/bin/python
#coding=utf-8

#from itertools import permutations
import itertools

def permutation_test1():
  for i in range(1,5):
    for j in range(1,5):
      for k in range(1,5):
        if (i != j) and (i != k) and (j != k):
          print i, j, k

def permutation_test2():
  for i in itertools.permutations([1,2,3,4], 3):
    print i

if __name__ == '__main__':
  permutation_test2()
