#!/usr/bin/python
import os
import gtk
import gtk.gdk
import glib

def clicked (data):
	(stdin, stdout) = os.popen2 ('../answer.py')
	stdin.write (question.get_text () + '\n')
	for a in answers:
		stdin.write (a.get_text () + '\n')
	stdin.write ('\n')
	stdin.flush ()
	print stdout.readlines ()

background_pixbuf = gtk.gdk.pixbuf_new_from_file('images/background.png')
gtk.rc_parse ('mvsm.gtkrc')

img = gtk.Image ()
img.set_from_pixbuf (background_pixbuf)
w = gtk.Window ()
fixed = gtk.Fixed ()
w.add (fixed)

options = []
answers = []

for i in range (0, 4):
	name = '%c: ' % (65 + i,)
	hbox = gtk.HBox ()
	e = gtk.Entry()
	hbox.add (gtk.Label (name))
	hbox.add (e)
	options += [hbox]
	answers += [e]

question = gtk.Entry ()
question.set_width_chars (52)
name = gtk.Label ('      Steve      ')

fixed.put (img, 0, 0)
fixed.put (options[0], 120, 258)
fixed.put (options[1], 348, 258)
fixed.put (options[2], 120, 300)
fixed.put (options[3], 348, 300)
fixed.put (question, 110, 190)

# name
name.set_alignment (xalign = 0, yalign = 0.5)
#name.set_size_request (95, -1)
#name.set_max_width_chars (15)
#name.set_width_chars (15)
fixed.put (name, 90, 62)

#ack button
ack = gtk.Button ()
ack_im = gtk.Image()
ack_im.set_from_file ('images/yes.png')
ack.set_relief (gtk.RELIEF_NONE)
#ack.set_size_request (100, -1)
ack.set_image (ack_im)
fixed.put (ack, 335, 345)

ack.connect ('clicked', clicked)

w.connect('destroy', gtk.main_quit)
w.show_all ()

gtk.main ()
