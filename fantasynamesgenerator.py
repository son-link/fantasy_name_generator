#!/usr/bin/python2
# -*- coding: utf-8 -*-

# Generador de nombres fantasticos
# Programado por Alfonso Saavedra "Son Link"
# http://sonlinkblog.blogspot.com
# Bajo licencia GPL 3
# 1 Beta 2

import sys, random, gtk, csv
import gettext, locale, json
from os import access, path, R_OK
from fng import fng

fng = fng.fng()

APP = 'fng'
gettext.textdomain (APP)
gettext.bindtextdomain (APP, './locale')
_ = gettext.gettext
gettext.install(APP, './locale', unicode=1)

class GUI():
	def __init__(self):
		# Comprobamos antes de nada que los 2 directorios existen y que tienen permisos de ejecucion
		if not access('names', R_OK):
			self.error_dialog(_("You don't have read permisions on names directory"))
			sys.exit(1)
		else:
			mainwin = gtk.Window()
			mainwin.set_title('Fantasy Names Generator')
			mainwin.set_position(gtk.WIN_POS_CENTER_ALWAYS)
			mainwin.set_default_size(400,300)

			hbox = gtk.HBox(homogeneous=False)

			vbox = gtk.VBox()

			lang_label = gtk.Label(str=_('Select race:'))
			lang_label.set_alignment(0, 0)
			vbox.pack_start(lang_label, False, False, 0)

			self.liststore = gtk.ListStore(str, str, bool)
			self.lang_select = gtk.ComboBox(self.liststore)
			cell = gtk.CellRendererText()
			self.lang_select.pack_start(cell, True)
			self.lang_select.add_attribute(cell, 'text', 1)
			self.liststore.append(['drow', _('Drow/Dark elf'), True])
			self.liststore.append(['elf', _('Elf'), False])
			self.liststore.append(['hafling', 'Hafling', True])
			self.liststore.append(['dwarven', _('Dwarven'), True])
			self.liststore.append(['gnome', _('Gnomes'), True])
			self.liststore.append(['demons', _('Demons'), False])
			self.liststore.append(['dragons', _(u'Dragons'), False])
			self.liststore.append(['orcs', _('Orcs'), False])
			self.lang_select.connect('changed', self.check_combobox)

			vbox.pack_start(self.lang_select, False, False, 0)

			sex_label = gtk.Label(str=_('Select sex:'))
			sex_label.set_alignment(0, 0)
			vbox.pack_start(sex_label, False, False, 0)

			liststore2 = gtk.ListStore(str, str)
			self.sex_select = gtk.ComboBox(liststore2)
			cell2 = gtk.CellRendererText()
			self.sex_select.pack_start(cell2, True)
			self.sex_select.add_attribute(cell2, 'text', 1)
			liststore2.append(['male', _('Male')])
			liststore2.append(['female', _('Female')])
			vbox.pack_start(self.sex_select, False, False, 0)
			self.sex_select.connect('changed', self.check_combobox)
			self.sex_select.set_sensitive(False)

			total_label = gtk.Label(str=_('Total generating (1-100):'))
			sex_label.set_alignment(0, 0)
			vbox.pack_start(total_label, False, False, 0)

			self.total_value = gtk.SpinButton()
			self.total_value.set_range(1, 100)
			self.total_value.set_increments(1.0, 5.0)
			vbox.pack_start(self.total_value, False, False, 0)

			self.generate = gtk.Button(label=_('Generate list'))
			self.generate.connect('clicked', self.generar)
			self.generate.set_sensitive(False)
			vbox.pack_start(self.generate, False, False, 0)

			self.save = gtk.Button(label=_('Save'))
			self.save.set_sensitive(False)
			self.save.connect('clicked', self.save_on_file)
			vbox.pack_start(self.save, False, False, 0)

			info = gtk.Button(label=_('About'))
			info.connect('clicked', self.view_info)
			vbox.pack_start(info, False, False, 0)

			hbox.pack_start(vbox, False, False, 0)

			textview_container = gtk.ScrolledWindow()
			self.textview = gtk.TextView()
			self.textview.set_editable(False)
			textview_container.add(self.textview)
			hbox.add(textview_container)

			mainwin.add(hbox)
			mainwin.show_all()
			mainwin.connect('destroy', self.destroy)

	def generar(self, w):
		race = self.lang_select.get_active_text()
		sex = self.sex_select.get_active_text()
		methodToCall = getattr(fng, race)

		self.textview.set_buffer(None)
		self.textbuffer = self.textview.get_buffer()
		i = 1
		total = int(self.total_value.get_text())
		for i in range(0, total):
			i += 1
			iter = self.textbuffer.get_end_iter()
			if self.sex_select.get_sensitive():
				self.textbuffer.insert(iter, methodToCall(race, sex)+"\n")
			else:
				self.textbuffer.insert(iter, methodToCall(race)+"\n")

		self.save.set_sensitive(True)

	def save_on_file(self, w):
		try:
			select_files = gtk.FileChooserDialog(title=_('Select where to save names'),action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_SAVE,gtk.RESPONSE_OK, gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
			filter = gtk.FileFilter()
			filter.set_name(_("Text"))
			filter.add_mime_type("text/plain")
			filter2 = gtk.FileFilter()
			filter2.set_name("CSV")
			filter2.add_mime_type("text/csv")
			select_files.add_filter(filter)
			select_files.add_filter(filter2)

			response = select_files.run()
			mime_name = select_files.get_filter().get_name()
			print mime_name
			if response == gtk.RESPONSE_OK:
				select_files.hide()
				if path.exists(select_files.get_filenames()[0]):
					warning = gtk.MessageDialog(parent=self.mainwin, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_YES_NO, message_format=_("Attention!"))
					warning.format_secondary_text(_('The file already exists.\nReplace?'))
					def close(w, res):
						if res == gtk.RESPONSE_NO:
							w.hide()
						elif res == gtk.RESPONSE_YES:
							w.hide()
							if mime_name == _("Text"):
								self.to_text(select_files.get_filenames()[0])
							elif mime_name == 'CSV':
								self.to_csv(select_files.get_filenames()[0])

					warning.connect("response", close)
					warning.run()
				if mime_name == _("Text"):
					self.to_text(select_files.get_filenames()[0])
				elif mime_name == 'CSV':
					self.to_csv(select_files.get_filenames()[0])

			else:
				select_files.hide()
		except IOError:
			self.error_dialog(_('An error occurred while saving the file.\nMake sure you have write permissions on the directory.'))

	def to_txt(self, filename):
		if not filename.endswith('.txt'):
			filename += '.txt'

		f = open(filename, 'w')
		txt = self.textbuffer.get_text(self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter())
		f.write(txt)
		f.close()

	def to_csv(self, filename):
		if not filename.endswith('.csv'):
			filename += '.csv'

		f = open(filename, 'w')
		csvfile = csv.writer(f, delimiter=',', quotechar='"')

		lines = self.textbuffer.get_line_count() - 1
		for l in range(0, lines):
			iter = self.textbuffer.get_iter_at_line(l)
			iter2 = self.textbuffer.get_iter_at_line(l + 1)
			name = self.textbuffer.get_text(iter, iter2).split('\n')[0].split()
			csvfile.writerow([name[0], name[1]])
		f.close()

	def view_info(self, widget):
		# esta funcion se limita a mostrar y cerrar el dialogo de la info
		info = gtk.AboutDialog()
		info.set_name('Fantastic Names Generator')
		info.set_version('1 beta 2')
		f = open('COPYING', 'r')
		info.set_license(f.read())
		info.set_comments(_("Generate names of many fantasy races"))
		info.set_website('http://sonlinkblog.blogspot.com')
		info.set_translator_credits(_('English: Son Link'))
		info.set_website_label(_("proyect's webpage"))
		def close(w, res):
			w.hide()
		info.connect("response", close)
		info.run()

	def error_dialog(self, message):
		warning = gtk.MessageDialog(parent=None, flags=0, type=gtk.MESSAGE_WARNING, buttons=gtk.BUTTONS_OK, message_format=_("Error!"))
		warning.format_secondary_text(message)
		def close(w, res):
			w.hide()
		warning.connect("response", close)
		warning.run()

	def check_combobox(self, w):
		model = self.lang_select.get_model()
		index = self.lang_select.get_active()
		if not model[index][2]:
			self.generate.set_sensitive(True)
			self.sex_select.set_sensitive(False)

		elif self.lang_select.get_active_text() and self.sex_select.get_active_text():
			self.generate.set_sensitive(True)
			self.sex_select.set_sensitive(True)

		else:
			self.sex_select.set_sensitive(True)

	def destroy(self, w):
		gtk.main_quit()

if __name__ == "__main__":
    GUI()
    gtk.main()
