#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  fnj.py
#
#  Copyright 2013 Alfonso Saavedra "Son Link" <sonlink@dhcppc4>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import json, random

class fnj:

	def __init__(self):
		pass

	def __getdata(self, race):
		f = open('../names/%s.json' % race)
		return json.loads(f.read())
		f.close()

	def dice(self, start=0, limit=0):
		return random.randint(start, limit)

	def drow_elf(self, race, sex='male'):
		data = self.__getdata(race)
		d10 = self.dice(1, 8)

		def __lastname():
			if d10 <= 3:
				return data['lastname_1'][self.dice(0, 29)] + data['lastname_2'][self.dice(0, 29)]

			elif d10 <= 5:
				return data['lastname_1'][self.dice(0, 29)] + data['lastname_2'][self.dice(0, 29)] + data['lastname_2'][self.dice(0, 29)]

			elif d10 <= 7:
				return data['lastname_1'][self.dice(0, 29)] + data['lastname_2'][self.dice(0, 29)] + "'" + data['lastname_2'][self.dice(0, 29)]

			elif d10 <= 9:
				return data['lastname_2'][self.dice(0, 29)] + "'" + data['lastname_1'][self.dice(0, 29)] + data['lastname_2'][self.dice(0, 29)]

		if d10 <= 3:
			name = data[sex+'_1'][self.dice(0, 99)] + data[sex+'_2'][self.dice(0,99)]

		elif d10 <= 5:
			name = data[sex+'_1'][self.dice(0, 99)] + data[sex+'_2'][self.dice(0,99)] + data[sex+'_2'][self.dice(0,99)]

		elif d10 <= 7:
			name =  data[sex+'_1'][self.dice(0,99)] +  data[sex+'_2'][self.dice(0,99)] + "'" +  data[sex+'_2'][self.dice(0,99)]
		else:
			name =  data[sex+'_2'][self.dice(0,99)] + "'" +  data[sex+'_1'][self.dice(0,99)] +  data[sex+'_2'][self.dice(0,99)]

		return name.capitalize() + ' ' + __lastname().capitalize()

	def dragons(self, race):
		data = self.__getdata(race)
		def __get_name():
			name = data['names'][self.dice(0,99)]
			if name.find('/') > -1:
				name = name.split('/')[self.dice(0, 1)]
			return name

		d20 = self.dice(1, 20)

		if d20 == 1:
			name = __get_name()
		elif d20 <= 12:
			name = __get_name() + __get_name()
		elif d20 <= 18:
			name = __get_name() + __get_name() + __get_name()
		else:
			name = __get_name() + __get_name() + ' ' + __get_name() + __get_name()

		return name.capitalize()

if __name__ == "__main__":
	fnj = fnj()
	for i in range(1, 20):
		print fnj.dragons('dragons')
