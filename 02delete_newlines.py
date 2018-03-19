#!/usr/bin/env python3
# coding: utf-8
"""
Внешняя команда для geany, восстанавливающая скопированный текст из pdf
"""
import sys

rules = (
    ('-\n', ''),
    ('\n', ' '),
)

if __name__ == '__main__':
    t = sys.stdin.read()
    for old, new in rules:
        t = t.replace(old, new)
    sys.stdout.write(t)
