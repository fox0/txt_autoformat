#!/usr/bin/env python3
# coding: utf-8
"""
Внешняя команда для geany, восстанавливающая скопированный текст из pdf
"""
import sys
import re

rules = (
    (r'\-\n', ''),
    (r'\n', ' '),
    (r'\s\[\d+\]', ''),
)

if __name__ == '__main__':
    t = sys.stdin.read()
    for old, new in rules:
        t = re.sub(old, new, t)
    sys.stdout.write(t)
