# pylint: skip-file
import pytest

from autoformat import replace_all, compile_pre, compile_post


@pytest.fixture()
def rules_pre():
    return compile_pre()


@pytest.fixture()
def rules_post():
    return compile_post()


def test_pre_true1(rules_pre):
    assert replace_all(rules_pre, 'кое кто') == 'кое-кто'


def test_pre_true2(rules_pre):
    assert replace_all(rules_pre, 'кое что') == 'кое-что'


def test_pre_true3(rules_pre):
    assert replace_all(rules_pre, 'кое как') == 'кое-как'


def test_pre_true4(rules_pre):
    assert replace_all(rules_pre, 'кое какой') == 'кое-какой'


def test_pre_true5(rules_pre):
    assert replace_all(rules_pre, 'кое какая') == 'кое-какая'


def test_pre_true6(rules_pre):
    assert replace_all(rules_pre, 'кое какого') == 'кое-какого'


def test_pre_true7(rules_pre):
    assert replace_all(rules_pre, 'кой кто') == 'кой-кто'


def test_pre_true8(rules_pre):
    assert replace_all(rules_pre, 'кой что') == 'кой-что'


def test_pre_true9(rules_pre):
    assert replace_all(rules_pre, 'КОЕ КТО') == 'КОЕ-КТО'


def test_pre_false1(rules_pre):
    assert replace_all(rules_pre, 'кое с чем') == 'кое с чем'


def test_pre2(rules_pre):
    assert replace_all(rules_pre, 'из за') == 'из-за'


def test_pre22(rules_pre):
    assert replace_all(rules_pre, 'из под') == 'из-под'


def test_pre3(rules_pre):
    assert replace_all(rules_pre, 'все таки') == 'всё-таки'
    assert replace_all(rules_pre, 'всё таки') == 'всё-таки'
    assert replace_all(rules_pre, 'все-таки') == 'всё-таки'
    assert replace_all(rules_pre, 'Все-таки') == 'Всё-таки'


# def test_pre31(rules_pre):
#    assert replace_all(rules_pre, 'ВСЕ ТАКИ') == 'ВСЁ-ТАКИ'


def test_pre4(rules_pre):
    assert replace_all(rules_pre, 'Понивилль') == 'Понивиль'
    assert replace_all(rules_pre, 'из Понивилля') == 'из Понивиля'
    assert replace_all(rules_pre, 'понивилльская библиотека') == 'Понивильская библиотека'


def test_pre5(rules_pre):
    assert replace_all(rules_pre, 'это наверное были они') == 'это, наверное, были они'
    assert replace_all(rules_pre, 'это, наверное были они') == 'это, наверное, были они'
    assert replace_all(rules_pre, 'это наверное, были они') == 'это, наверное, были они'
    assert replace_all(rules_pre, 'это. Наверное были они') == 'это. Наверное, были они'
