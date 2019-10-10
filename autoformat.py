#!/usr/bin/env python3
import argparse
import re
import sys


def compile_rules(ls):
    result = []
    for expr, new_val in ls:
        try:
            result.append((re.compile(expr, re.I), new_val))
        except Exception as ex:
            sys.stderr.write('error compile: %s. expr=%s' % (ex, expr))
    return result


def replace_all(rules, text):
    result = text.strip()
    for expr, new_val in rules:
        result = expr.sub(new_val, result)
    return result


def compile_pre():
    result = []
    prefix = '|'.join(('[кч]то', 'как', r'как\w{2,3}', 'где', 'чем', 'чей',
                       'чему', 'чего', 'куда', 'кому', 'кого', 'зачем', 'когда'))
    result.extend((
        # кое-
        (r'\b(ко[ей]) (%s)\b' % prefix, r'\1-\2'),
        # -либо
        (r'\b(%s|откуда|почему|отчего) (либо)\b' % prefix, r'\1-\2'),
        # -то
        (r'\b(%s|так|кои|общем|почему|вообще|наконец) (то)\b' % prefix, r'\1-\2'),
    ))
    del prefix

    result.extend((
        (r'\b(во) (первых|вторых)\b', r'\1-\2'),
        (r'\b(из) (за|под)\b', r'\1-\2'),
        # -таки
        (r'\b(вс[её]|довольно) (таки)\b', r'\1-\2'),  # после наречий, частиц и глаголов соединяется с ними дефисом
        (r'\b(в)се-таки\b', r'\1сё-таки'),
        # -нибудь
        # -ка
        (r'\s(нибудь|ка)\b', r'-\1'),
        # not dash
        (r'-(бы|же|ли|уж|лишь)\b', r' \1'),
        # всё
        (r'\b(в)се (еще|ещё|ж|же|равно|так же)\b', r'\1сё \2'),
        # автозамена популярных опечаток
        (r'\b(не)(а)\b', r'\1-\2'),
        (r'\bнеспеша\b', 'не спеша'),
        (r'\bчерез чур\b', 'чересчур'),
        (r'\bс подряд\b', 'подряд'),
        (r'\bсосем\b', 'совсем'),
        (r'\bуверенна\b', 'уверена'),
        (r'\bво-время\b', 'вовремя'),
        (r'\bсхмурив\b', 'нахмурив'),
        (r'\bшопот\b', 'шёпот'),
        (r'\bладо\b', 'ладно'),
        (r'\bтрамв', 'травм'),
        (r'\bсеръ', 'серь'),
        # имена
        (r'\bТва[йл][йла]?[ла]?[йт][йт]\b', 'Твайлайт'),
        (r'\bРейнбоу\b', 'Рэйнбоу'),
        # todo каденс
        # (r'\bЭпп?л\s*Блум\b', 'Эплблум'),
        (r'\bМундансер\b', 'Мундэнсер'),
        (r'\bБон-Бон\b', 'Бон Бон'),
        (r'\bпонивилл', 'Понивил'),

        (r'\.-', '. -'),
        (r',-', ', -'),
        (r' -…', ' - …'),
        (r'</i><i>', ''),
        (r'\s+</i>', '</i>'),
        (r'\s*\n\s*', '\n\n'),
    ))

    def colon(m):
        dot = m.group(1) or ','
        word = m.group(2)
        dot2 = m.group(3) or ','
        return '%s %s%s' % (dot, word, dot2)

    ls = '|'.join(('впрочем', 'наверное', 'видимо', 'пожалуй', 'по крайней мере', 'как правило', 'скоре[ей] всего'))
    result.append((r'\b([,\.]?)\s+(%s)\b([,…!\.\?])?' % ls, colon))
    return compile_rules(result)


def compile_post():
    result = [
        (r'…[…\.]', '…'),
        (r'(\?|!)…', r'\1..'),
        (r'…(\?|!)', r'\1..'),
        (r'\.\.(\?|!)', r'\1..'),
        (r'[!\?]\?', '?!'),
        # нет пробелам после многоточия
        (r'\n…\s+', '\n…'),
        # fix wiki
        (r"'''(.*?)'''", r'<b>\1</b>'),
        (r"''(.*?)''", r'<i>\1</i>'),
        (r'</b><b>', ''),
        (r'\bбёлль\b', 'Белль'),
        # fix3
        (r'<center>\*\s*\*\s*\*</center>', '***'),
        (r'\n\*{3}\s*\n', '\n\n<center>* * *</center>\n'),
        (r'^<tab>', ''),
        (r'<tab>$', ''),
    ]

    mdash = '—'
    nbsp = '\xa0'
    result.extend((
        (r'…-', '… ' + mdash),
        (r'\n-', '\n' + mdash + nbsp),
        (r'\n<i>-\s+', '\n<i>' + mdash + nbsp),
        # неразрывный пробел после тире
        (r'\n%s\s+' % mdash, '\n' + mdash + nbsp),
    ))

    return compile_rules(result)


TEMPLATE = '''\
<tab>
{text}
<tab>

--
Число слов: {count}'''


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--pre', action='store_true')
    group.add_argument('--post', action='store_true')
    args = parser.parse_args()

    text = sys.stdin.read()
    if args.pre:
        rules = compile_pre()
        text = replace_all(rules, text)
    elif args.post:
        rules = compile_post()
        text = replace_all(rules, text)
        count_words = len(re.findall(r'\w+', text))
        text = TEMPLATE.format(text=text, count=count_words)
    sys.stdout.write(text)


if __name__ == '__main__':
    main()
