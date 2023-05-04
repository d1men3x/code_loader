#!/usr/bin/python3

import random
from time import sleep

for i in range(0, 993, 7):
    print('<     %i - 7 = %i    >' % (1000-i, 1000-(i+7)),end='\r\r')
    sleep(0.3)
print('\n')