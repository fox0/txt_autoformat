#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys


def compile_rules(*ruleset):
    result = []
    for expr, new_val in ruleset:
        try:
            result.append((re.compile(expr, re.I), new_val))
            # print(expr, new_val)
        except Exception as e:
            sys.stderr.write('error compile: %s. expr=%s' % (e, expr))
    return result


def replace_all(rules, text):
    result = text.strip()
    for expr, new_val in rules:
        result = expr.sub(new_val, result)
    return result


rules_pre = compile_rules(
    # dash
    (r'\b(во)\s(первых|вторых)\b', r'\1-\2'),
    (r'\b(из)\s(за|под)\b', r'\1-\2'),
    (r'\b(как\w{2,3}|как|кои|кто|что|чем|где|чей|так|кого|куда|чего|чему|кому|общем|когда|почему|вообще|наконец)\s(то)\b', r'\1-\2'),
    (r'\b(кое)\s(как|что|чего)\b', r'\1-\2'),
    (r'\b(что)\s(либо)\b', r'\1-\2'),
    (r'\s(нибудь|ка)\b', r'-\1'),
    (r'\b(н)еа\b', r'\1е-а'),
    (r'\b(все|всё|довольно)\s(таки)\b', r'\1-\2'),  # после наречий, частиц и глаголов соединяется с ними дефисом
    
    (r'\bчерез\sчур\b', 'чересчур'),
    (r'\bс\sподряд\b', 'подряд'),
    (r'\bв\sсамом\sделе\b', 'правда'),
    (r'\bпонивилль\b', 'Понивиль'),

    # not dash
    (r'-(бы|же|ли|уж|что|лишь)\b', r' \1'),
    # common
    (r'<center>\*{3}</center>', '***'),
    (r'\*{3}', '\n<center>* * *</center>'),
    (r'\n\s+', '\n\n'),
    # ~ (r'<tab>', ''),
)

# u = ' '  # '\u00A0'; // non-breaking space
m = '—'  # mdash

rules_post = compile_rules(
    (r'(\?|!)…', r'\1..'),
    (r'…(\?|!)', r'\1..'),
    (r'\.\.(\?|!)', r'\1..'),
    
    (r'\?\?', '?!'),
    (r'…\.', '…'),
    
    # ё
    (r'\b(в)се-таки\b', r'\1сё-таки'),
    (r'\b(в)се\s(ещё|ж|же|равно)\b', r'\1сё \2'),
    (r'\bбёлль\b', 'Белль'),
    
    (r'^<tab>', ''),
    (r'<tab>$', ''),
    
    # fix wiki
    (r"'''(.*?)'''", r'<b>\1</b>'),
    (r"''(.*?)''", r'<i>\1</i>'),
    
    (r'\n-(\w)', r'\n'+m+r' \1'),
    # ~ (r'\n<tab>—\s+', '\n<tab>—'+u),
    # ~ (r'\n-<tab>', '\n<tab>—'+u),
    (r'\n<i>-', '\n<i>'+m),
    
    # ~ (r'\n+', '\n\n<tab>'),
)


template = '''\
<tab>
%s
<tab>

--
Число слов: %d

(%d символов без пробелов)'''


if __name__ == '__main__':
    if sys.argv[1] == '--pre':
        text = sys.stdin.read()
        text = replace_all(rules_pre, text)
        sys.stdout.write(text)
    elif sys.argv[1] == '--post':
        text = sys.stdin.read()
        text = replace_all(rules_post, text)
        count_words = len(re.findall(r'\w+', text))
        count_ch = len(re.sub(r'\s+', '', text))
        text = template % (text, count_words, count_ch)
        sys.stdout.write(text)
    else:
        raise NotImplementedError
