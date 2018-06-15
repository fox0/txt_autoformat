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
    ('все еще', 'всё ещё'),
    ('все ещё', 'всё ещё'),
    ('нее', 'неё'),
    ('мое', 'моё'),
    ('все-таки', 'всё-таки'),
    ('все таки', 'всё-таки'),
    ('насчет', 'насчёт'),

    # todo func " " -> "-"
    ('из за', 'из-за'),
    ('из под', 'из-под'),
    ('кое как', 'кое-как'),
    
    ('кто то', 'кто-то'),
    ('что то', 'что-то'),

    ('наконец то', 'наконец-то'),  # "Наконец то" todo
    ('вообще то', 'вообще-то'),
    ('когда то', 'когда-то'),
    ('куда то', 'куда-то'),
    ('чего то', 'чего-то'),
    ('как то', 'как-то'),
    ('кое чего', 'кое-чего'),
    ('общем то', 'общем-то'),
    
    ('во первых', 'во-первых'),
    ('во вторых', 'во-вторых'),

) + compile_rules(
    (r'\bкак(\w{2,3})\sто\b', r'как\1-то'),
    (r'\sнибудь\b', '-нибудь'),
    (r'<center>\*{3}</center>', '***'),
    (r'\*{3}', '\n<center>* * *</center>'),
    (r'\n\s+', '\n\n'),
)


def fucking_dot(m):
    s1, s2, s3 = m.group(1), m.group(2), m.group(3)
    s2 = {'.': ','}.get(s2, s2)
    s3 = s3.lower()
    return '\n— %s%s — %s' % (s1, s2, s3)
    

rules_post = compile_rules(
    (r"'''(.*?)'''", r'<b>\1</b>'),
    (r"''(.*?)''", r'<i>\1</i>'),
    (r'\n—\s(.*?)([\.\?!…])\s—\s(\w)', fucking_dot),
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
