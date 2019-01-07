#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys


def compile_rules(*ruleset):
    result = []
    for expr, new_val in ruleset:
        try:
            result.append((re.compile(expr, re.I), new_val))
        except Exception as e:
            sys.stderr.write('error compile: %s. expr=%s' % (e, expr))
    return result


def replace_all(rules, text):
    result = text.strip()
    for expr, new_val in rules:
        result = expr.sub(new_val, result)
    return result


prefix = '|'.join(('[кч]то', 'как\w{2,3}', 'как', 'где', 'чем', 'чей',
                   'чему', 'чего', 'куда', 'кому', 'кого', 'зачем', 'когда'))

rules_pre = compile_rules(
    (r'\b(во)\s(первых|вторых)\b', r'\1-\2'),
    (r'\b(из)\s(за|под)\b', r'\1-\2'),
    # кое-
    (r'\b(ко[ей])\s(%s)\b' % prefix, r'\1-\2'),
    # -либо
    (r'\b(%s)\s(либо)\b' % prefix, r'\1-\2'),
    # -то
    (r'\b(%s|так|кои|общем|почему|вообще|наконец)\s(то)\b' % prefix, r'\1-\2'),
    # -таки
    (r'\b(вс[её]|довольно)\s(таки)\b', r'\1-\2'),  # после наречий, частиц и глаголов соединяется с ними дефисом
    (r'\b(в)се-таки\b', r'\1сё-таки'),
    # -нибудь
    # -ка
    (r'\s(нибудь|ка)\b', r'-\1'),
    # ...
    (r'\b(н)еа\b', r'\1е-а'),
    (r'\bнеспеша\b', 'не спеша'),
    (r'\bчерез\sчур\b', 'чересчур'),
    (r'\bс\sподряд\b', 'подряд'),
    (r'\bпонивилль', 'Понивиль'),
    # ...
    (r'-(бы|же|ли|уж|лишь)\b', r' \1'),
    (r'\b(в)се\s(еще|ещё|ж|же|равно|так\sже)\b', r'\1сё \2'),
)


m = '—'  # mdash
# u = ' '  # '\u00A0'; // non-breaking space

rules_post = compile_rules(
    (r'\s+\n', '\n\n'),

    (r'(\?|!)…', r'\1..'),
    (r'…(\?|!)', r'\1..'),
    (r'\.\.(\?|!)', r'\1..'),
    (r'\?\?', '?!'),
    (r'…\.', '…'),

    (r'\bбёлль\b', 'Белль'),

    (r'<center>\*{3}</center>', '***'),
    (r'\*{3}', '\n<center>* * *</center>'),

    # fix wiki
    (r"'''(.*?)'''", r'<b>\1</b>'),
    (r"''(.*?)''", r'<i>\1</i>'),

    (r'\n-(\w)', r'\n%s \1' % m),
    (r'\n<i>-', '\n<i>%s' % m),
    # ~ (r'\n<tab>—\s+', '\n<tab>—'+u),
    # ~ (r'\n-<tab>', '\n<tab>—'+u),

    (r'^<tab>', ''),
    (r'<tab>$', ''),
)


def run_test():
    tests_pre = (
        ('во первых', 'во-первых'),
        ('Во первых', 'Во-первых'),
        ('слово во первых нам', 'слово во-первых нам'),
        ('во вторых', 'во-вторых'),
        ('из за', 'из-за'),
        ('из под', 'из-под'),
        )
    prefix = ('кто', 'что', 'какая', 'какой', 'какого', 'как', 'где', 'чем', 'чей',
              'чему', 'чего', 'куда', 'кому', 'кого', 'зачем', 'когда')
    tests_pre += tuple(('кое %s' % i, 'кое-%s' % i) for i in prefix)
    tests_pre += (
        ('кое с чем', 'кое с чем'),
        )
    tests_pre += tuple(('%s либо' % i, '%s-либо' % i) for i in prefix)
    tests_pre += (
        ('откуда либо', 'откуда-либо'),
        ('отчего либо', 'отчего-либо'),
        ('почему либо', 'почему-либо'),
        )
    tests_pre += tuple(('%s то' % i, '%s-то' % i) for i in prefix)
    tests_pre += tuple(('%s то' % i, '%s-то' % i) for i in ('так', 'кои', 'общем', 'почему', 'вообще', 'наконец'))
    tests_pre += (
        ('все таки', 'всё-таки'),
        ('всё таки', 'всё-таки'),
        ('все-таки', 'всё-таки'),
        ('довольно таки', 'довольно-таки'),
        ('как нибудь', 'как-нибудь'),
        ('что нибудь', 'что-нибудь'),
        # todo
        ('', ''),

        ('Понивилль', 'Понивиль'),
        ('понивилльская библиотека', 'Понивильская библиотека'),

        ('', ''),
    )

    tests_post = (
        ('текст    \nтекст2', 'текст\n\nтекст2'),
        ('текст\n\nтекст2', 'текст\n\nтекст2'),
        ('текст\n\n\nтекст2', 'текст\n\nтекст2'),
        ('', ''),
    )

    ls = (rules_pre, tests_pre), (rules_post, tests_post)
    print('run %d tests...' % (sum(map(lambda x: len(x[1]), ls))))
    for rules, tests in ls:
        for i, (t, t2) in enumerate(tests):
            r = replace_all(rules, t)
            if r != t2:
                print('error #%3.d: "%s" != "%s"' % (i, t2, r))


template = '''\
<tab>
%s
<tab>

--
Число слов: %d

(%d символов без пробелов)'''


if __name__ == '__main__':
    if len(sys.argv) == 2:
        text = sys.stdin.read()
        if sys.argv[1] == '--pre':
            text = replace_all(rules_pre, text)
        elif sys.argv[1] == '--post':
            text = replace_all(rules_post, text)
            count_words = len(re.findall(r'\w+', text))
            count_ch = len(re.sub(r'\s+', '', text))
            text = template % (text, count_words, count_ch)
        else:
            raise NotImplementedError
        sys.stdout.write(text)
    elif len(sys.argv) == 1:
        run_test()
