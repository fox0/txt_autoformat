#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import sys
import subprocess


BASE_DIR = os.path.dirname(__file__)

rules_pre = []
rules_post = []


def compile_rules(*ruleset):
    result = []
    for expr, new_val in ruleset:
        try:
            result.append((re.compile(expr, re.I), new_val))
            # print(expr, new_val)
        except Exception as e:
            sys.stderr.write('error compile: %s. expr=%s' % (e, expr))
    return result


rules_pre += compile_rules(
    (r'\s(нибудь|ка)\b', r'-\1'),
    (r'\b(как\w{2,3}|кто|что|чем|где|чей|как|кого|куда|чего|чему|общем|когда|почему|вообще|наконец)\s(то)\b', r'\1-\2'),
    (r'\b(во)\s(первых|вторых)\b', r'\1-\2'),
    (r'\b(из)\s(за|под)\b', r'\1-\2'),
    (r'\b(кое)\s(как|что|чего)\b', r'\1-\2'),
    (r'\b(все|всё)\s(таки)\b', r'\1-\2'),  # после наречий, частиц и глаголов соединяется с ними дефисом
    
    (r'<center>\*{3}</center>', '***'),
    (r'\*{3}', '\n<center>* * *</center>'),
    (r'\n\s+', '\n\n'),
)


def fucking_dot(m):
    s1, s2, s3 = m.group(1), m.group(2), m.group(3)
    s2 = {'.': ','}.get(s2, s2)
    s3 = s3.lower()
    return '\n— %s%s — %s' % (s1, s2, s3)
    

rules_post += compile_rules(
    (r'\n—\s(.*?)([\.\?!…])\s—\s(\w)', fucking_dot),
    (r'\?…', '?..'),
    (r'!…', '!..'),
    (r'\bвсе\sещё\b', 'всё ещё'),
    (r'\bвсе\sтаки\b', 'всё-таки'),
    
    # fix wiki
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
    text = run_js(text, 'wikificator.js')
    text = run_js(text, 'node_modules/eyo/bin/cli.js', '--stdin')
    text = replace_all(rules_post, text)

    count_words = len(re.findall(r'\w+', text))
    count_ch = len(re.sub(r'\s+', '', text))
    return template % (text, count_words, count_ch)


def replace_all(re_rules, text):
    result = text.strip()
    for expr, new_val in re_rules:
        result = expr.sub(new_val, result)
    return result


def run_js(text, filename, *args):
    f = os.path.join(BASE_DIR, filename)
    b = bytes(text.encode('utf-8'))
    return subprocess.check_output(('js', f, *args), input=b).decode('utf-8')


if __name__ == '__main__':
    text_in = sys.stdin.read()
    text_out = main(text_in)
    sys.stdout.write(text_out)
