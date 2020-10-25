#!/usr/bin/python
# -*- coding: utf-8 -*-

# Generador de nombres fantásticos
# Programado por Alfonso Saavedra "Son Link"
# http://son-link.github.io
# Bajo licencia GPL 3
# 1.0.0

import sys, random, csv
import locale, json, re
from os import access, path, R_OK
from fng import fng
from gui import *
from PyQt5.QtCore import QLocale, QTranslator
fng = fng.fng()

_translate = QtCore.QCoreApplication.translate
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi(self)

		self.setWindowIcon(QtGui.QIcon('icon.svg'))

		self.btGen.clicked.connect(self.generate)
		self.btSave.clicked.connect(self.save_to_file)
		self.cbRace.currentIndexChanged.connect(self.raceChange)

		self.races = [
			('drow', True),
			('elf', False),
			('hafling', True),
			('dwarven', True),
			('gnome', True),
			('demons', False),
			('dragons', False),
			('orcs', False)
		]

		self.sex = ['male', 'female']

	def raceChange(self):
		pos = self.cbRace.currentIndex()
		sex = self.races[pos][1]
		if (sex):
			self.cbSex.setEnabled(True)
		else:
			self.cbSex.setEnabled(False)


	def generate(self):
		race_pos = self.cbRace.currentIndex()
		sex_pos = self.cbRace.currentIndex()
		race = self.races[race_pos][0]
		sex = self.sex[sex_pos]
		total = self.sbTotal.value()

		self.listNames.clear()

		methodToCall = getattr(fng, race)
		for i in range(0, total):
			if self.cbSex.isEnabled():
				self.listNames.addItem(methodToCall(race, sex))
			else:
				self.listNames.addItem(methodToCall(race))

		self.btSave.setEnabled(True)
		
	def save_to_file(self):
		fileDialog = QtWidgets.QFileDialog(self)
		fileDialog.setOptions(QtWidgets.QFileDialog.DontUseNativeDialog)
		filename, _ = fileDialog.getSaveFileName(self,_translate("save_to_file", 'Save names'),"",_translate('MainWindow', "Text Files (*.txt)"))
		if filename:
			try:
				if not filename.endswith('.txt'):
					filename += '.txt'

				f = open(filename, 'w')
				for i in range(self.listNames.count()):
					f.write(self.listNames.item(i).text()+"\n")
				f.close()
			except IOError:
				msg = _translate('MainWindow', _translate('MainWindow', 'An error occurred while saving the file.\nMake sure you have write permissions on the directory.'))
				self.show_error(_translate('MainWindow', 'Error'), msg)
				

	def show_error(self, title, text):
		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Critical)

		msg.setText(text)
		msg.setWindowTitle(title)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok )
		msg.exec_()

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	LOCAL_DIR = path.dirname(path.realpath(__file__))
	defaultLocale = QLocale.system().name()
	if defaultLocale == 'es_ES':
		defaultLocale = 'es'
	
	translator = QtCore.QTranslator()
	
	translator.load(LOCAL_DIR + "/locale/" + defaultLocale + ".qm")
	app.installTranslator(translator)
	window = MainWindow()
	window.retranslateUi(window)
	window.show()
	app.exec_()
