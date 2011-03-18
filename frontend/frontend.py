#!/usr/bin/python
import gtk
import gtk.gdk
import glib

background_pixbuf = gtk.gdk.pixbuf_new_from_file('images/background.png')
gtk.rc_parse ('mvsm.gtkrc')

img = gtk.Image ()
img.set_from_pixbuf (background_pixbuf)
w = gtk.Window ()
fixed = gtk.Fixed ()
w.add (fixed)

options = []

for i in range (0, 4):
	name = '%c: ' % (65 + i,)
	hbox = gtk.HBox ()
	hbox.add (gtk.Label (name))
	hbox.add (gtk.Entry ())
	options += [hbox]
question = gtk.Entry ()
question.set_width_chars (52)

fixed.put (img, 0, 0)
fixed.put (options[0], 120, 258)
fixed.put (options[1], 348, 258)
fixed.put (options[2], 120, 300)
fixed.put (options[3], 348, 300)
fixed.put (question, 110, 190)

w.connect('destroy', gtk.main_quit)
w.show_all ()

gtk.main ()
