# coding=utf-8
from random import randint

__author__ = 'adrian'
k = ["a", "b", "c", "d"]
l = []
while len(l) <= 3:
    r = randint(0, 3)
    if r not in l:
        l.append(r)
print(l)
r = [0]*4
for e, i in zip(k, l):
    r[i] = e
print r
