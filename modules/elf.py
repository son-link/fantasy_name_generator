#!/usr/bin/python
# -*- coding: utf-8 -*-
# Drow Names Generator
# Under GNU/GPL v3
# (C) 2011 Alfonso Saavedra "Son Link"

import random
class Generator():
	def __init__(self):
		self.limit = False
		self.table_1 = []
		self.table_2 = []
		self.table_3 = []
		self.table_4 = []
		
		names_1 = open('txt/elf_1.txt', 'r')
		for line in names_1.readlines():
			self.table_1.append(line.split()[0])
			
		names_2 = open('txt/elf_2.txt', 'r')
		for line in names_2.readlines():
			self.table_2.append(line.split()[0])
			
		house_1 = open('txt/elf_house_1.txt', 'r')
		for line in house_1.readlines():
			self.table_3.append(line.split()[0])
			
		house_2 = open('txt/elf_house_2.txt', 'r')
		for line in house_2.readlines():
			self.table_4.append(line.split()[0])

	def d100(self):
		return int(random.randint(0, 99))
	
	def d30(self):
		return int(random.randint(0, 29))

	def generate(self):
		d10 = random.randint(1, 10)
		if d10 <= 3:
			name = self.table_1[self.d100()] + self.table_2[self.d100()]
				
		elif d10 <= 5:
			name = self.table_1[self.d100()] + self.table_2[self.d100()] + self.table_2[self.d100()]
				
		elif d10 <= 7:
			name = self.table_1[self.d100()] + self.table_2[self.d100()] + "'" + self.table_2[self.d100()]
			
		elif d10 <= 9:
			if not self.limit:
				name = self.table_1[self.d100()] + self.table_2[self.d100()] + ' ' + self.generate() + ' '
				self.limit = True
			else:
				name = self.table_1[self.d100()] + self.table_2[self.d100()]
		else:
			name = self.table_2[self.d100()] + "'" + self.table_1[self.d100()] + self.table_2[self.d100()]
			
		return name.capitalize() + ' ' + self.generate_house_name().capitalize()
			
	def generate_house_name(self):
		d10 = random.randint(1, 9)
		if d10 <= 3:
			return self.table_3[self.d30()] + self.table_4[self.d30()]
				
		elif d10 <= 5:
			return self.table_3[self.d30()] + self.table_4[self.d30()] + self.table_4[self.d30()]
				
		elif d10 <= 7:
			return self.table_3[self.d30()] + self.table_4[self.d30()] + "'" + self.table_4[self.d30()]
			
		elif d10 <= 9:
			return self.table_4[self.d30()] + "'" + self.table_3[self.d30()] + self.table_4[self.d30()]
			
