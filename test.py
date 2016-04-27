# -*- coding: utf-8 -*-
import mpinyin

print("import done")
py = mpinyin.Pinyin()
print("create new Pinyin() doen")
py.load()
print("load done")
print(py.get_max_py('中国银行行长'))
print(py.get_max_py('红花绿叶的传说', tone=mpinyin.NUM_TONE))
print(py.get_max_py('红花绿叶的传说', tone=mpinyin.MARK_TONE))
print(py.get_max_py('猿题库', tone=mpinyin.NUM_TONE))
print(py.get_max_py('猿题库', tone=mpinyin.MARK_TONE))
print(py.get_max_py('联想Y470电脑', tone=mpinyin.MARK_TONE))
