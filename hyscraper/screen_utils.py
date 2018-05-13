#!/usr/bin/env python3
import time

def clear_screen():
    print('\033[H\033[J')

def newlines(number=1):
    if number == 1:
        print('')
    elif number == 2:
        print('\n')
    else:
        number -= 1
        print('\n' * number)

def roll_the_screen(number):
    for i in range(number):
        print('')
        time.sleep(0.05)
