#!/usr/bin/python
# -*- coding: utf-8 -*-
# Drow Names Generator
# Under GNU/GPL v3
# (C) 2011 Alfonso Saavedra "Son Link"

from random import randint

class Generator():
	def __init__(self, sex):
		self.sex = sex
		self.limit = False
		self.table_1 = []
		self.table_2 = []
		self.table_3 = []
		
		names = open('txt/'+self.sex+'_halfling.txt', 'r')
		for line in names.readlines():
			self.table_1.append(line.split()[0])
			
		house_1 = open('txt/halfling_surnames_1.txt', 'r')
		for line in house_1.readlines():
			self.table_2.append(line.split()[0])
			
		house_2 = open('txt/halfling_surnames_2.txt', 'r')
		for line in house_2.readlines():
			self.table_3.append(line.split()[0])

	def generate(self):
		n = randint(0, len(self.table_1[1:]))
		name = self.table_1[n]
			
		return name + ' ' + self.generate_house_name()
			
	def generate_house_name(self):
		
		n = randint(0, len(self.table_2[1:]))
		s = randint(0, len(self.table_3[1:]))
		
		return self.table_2[n] + self.table_3[s]
