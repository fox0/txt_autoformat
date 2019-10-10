#!/usr/bin/env python3
"""
Внешняя команда для geany, восстанавливающая скопированный текст из pdf
"""
import re
import sys


def main():
    text = sys.stdin.read()
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s\[\d+\]', '', text)
    sys.stdout.write(text)
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
