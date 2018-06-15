#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import sys
import subprocess


def compile_rules(*ruleset):
    result = []
    for expr, new_val in ruleset:
        try:
            result.append((re.compile(expr), new_val))
        except Exception as e:
            sys.stderr.write('error compile: %s. expr=%s' % (e, expr))
    return result


def compile_rules_word(*ruleset):
    result = []
    for old, new in ruleset:
        result.append((r'\b%s\b' % old, new))
        result.append((r'\b%s\b' % old.title(), new.title()))
    return compile_rules(*result)


rules_pre = compile_rules_word(
    ('ее', 'её'),
    ('еще', 'ещё'),
    ('нее', 'неё'),
    ('мое', 'моё'),
    ('все-таки', 'всё-таки'),
    ('насчет', 'насчёт'),

    ('из за', 'из-за'),
    ('кто то', 'кто-то'),
    ('из под', 'из-под'),

) + compile_rules(
    (r'<center>\*{3}</center>', '***'),
    (r'\*{3}', '\n<center>* * *</center>'),
)

rules_post = compile_rules(
    (r"'''(.*?)'''", r'<b>\1</b>'),
    (r"''(.*?)''", r'<i>\1</i>'),
)

template = '''\
<tab>
%s
<tab>

--
Число слов: %d

(%d символов без пробелов)'''


def main(text):
    text = replace_all(rules_pre, text)
    text = run_wikificator(text)
    text = replace_all(rules_post, text)

    count_words = len(re.findall(r'\w+', text))
    count_ch = len(re.sub(r'\s+', '', text))
    return template % (text, count_words, count_ch)


def replace_all(re_rules, text):
    result = text.strip()
    for expr, new_val in re_rules:
        result = expr.sub(new_val, result)
    return result


def run_wikificator(text):
    f = os.path.join(os.path.dirname(__file__), 'wikificator.js')
    b = bytes(text.encode('utf-8'))
    return subprocess.check_output(('js', f), input=b).decode('utf-8')


if __name__ == '__main__':
    text_in = sys.stdin.read()
    text_out = main(text_in)
    sys.stdout.write(text_out)
