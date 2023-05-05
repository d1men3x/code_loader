#!/usr/bin/python3

from time import sleep

for i in range(0, 993, 7):
    print('<     %i - 7 = %i    >' % (1000-i, 1000-(i+7)),end='\r')
    sleep(0.3)
print('\n')