#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pequeño script para pasar minuscula a latra capital
f= open('elf_house_1.txt', 'r')
o = open('elf_1-2.txt', 'w')
for line in f.readlines():
	txt = line.split('/')[0]
	o.write(line.lower())
f.close()
o.close()
