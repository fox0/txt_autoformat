#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import subprocess
from os.path import dirname, join


def compile_rules(*ruleset):
    result = []
    for expr, new_val in ruleset:
        try:
            result.append((re.compile(expr), new_val))
        except Exception as e:
            sys.stderr.write('error compile: %s. expr=%s' % (e, expr))
    return result


re_text_pre = compile_rules(
    (r'\/\*.*?\*\/', ''),  # /* ... */
    (r'\n+', '\n\n'),
    (r'<tab>', ''),
)

re_line = compile_rules(
    (r'^[\s01]+$', ''),
    (r'^\*{3}$', '\n<center>* * *</center>'),
)

_words = (
    ('ее', 'её'),
    ('еще', 'ещё'),
    ('нее', 'неё'),
    ('мое', 'моё'),
    ('все-таки', 'всё-таки'),
    ('насчет', 'насчёт'),
)
re_words = [
    (r"''(.*?)''", r'<i>\1</i>'),
]
for v, n in _words:
    re_words.append((r'\b%s\b' % v, n))
    re_words.append((r'\b%s\b' % v.title(), n.title()))
re_text_post = compile_rules(*re_words)
del _words
del re_words


def main(text):
    # text = replace_all(re_text_pre, text)
    text = '\n'.join([replace_all(re_line, line) for line in text.split('\n')])
    f = join(dirname(__file__), 'wikificator.js')
    text = run_process(('js', f), text)
    # todo ё-фикатор
    text = replace_all(re_text_post, text)
    text = text.replace('И. И.', 'И.И.')
    return '''\
<tab>
%s
<tab>

Число слов: %d''' % (text, len(text.split(' ')))


def replace_all(re_rules, text):
    result = text.strip()
    for expr, new_val in re_rules:
        result = expr.sub(new_val, result)
    return result


def run_process(cmd, data):
    bytes_in = bytes(data.encode('utf-8'))
    bytes_out = subprocess.check_output(cmd, input=bytes_in)
    return bytes_out.decode('utf-8')


if __name__ == '__main__':
    text_in = sys.stdin.read()
    text_out = main(text_in)
    sys.stdout.write(text_out)
