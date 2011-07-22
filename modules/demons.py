#!/usr/bin/python
# -*- coding: utf-8 -*-
# Drow Names Generator
# Under GNU/GPL v3
# (C) 2011 Alfonso Saavedra "Son Link"

from random import randint

class Generator():
	def __init__(self):
		
		self.table_1 = []
		self.table_2 = []
		
		names_1 = open('txt/demon_1.txt', 'r')
		for line in names_1.readlines():
			self.table_1.append(line.split()[0])
		
		names_2 = open('txt/demon_2.txt', 'r')
		for line in names_2.readlines():
			self.table_2.append(line.split()[0])
			
	def generate(self):
		n = randint(0, len(self.table_1[1:]))
		s = randint(0, len(self.table_2[1:]))
		return self.table_1[n].split()[0] + self.table_2[s].split()[0]
