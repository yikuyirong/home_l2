

#!usr/bin/env python3

# -*- coding:utf-8 -*-


def check(num):

    if num < 10 :
        return False

    s = str(num)

    return s == "".join(reversed(s))


F = filter(check,list(range(10000)))


print(list(F))
