#!/usr/bin/python
# -*- coding: utf-8 -*-
# Drow Names Generator
# Under GNU/GPL v3
# (C) 2011 Alfonso Saavedra "Son Link"

from random import randint

class Generator():
	def __init__(self):
		self.table_1 = []
		
		names = open('txt/orcs.txt', 'r')
		for line in names.readlines():
			self.table_1.append(line.split()[0])
			
	def generate(self):
		n = randint(0, len(self.table_1[1:]))
		return self.table_1[n].split()[0]
			
