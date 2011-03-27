#!/usr/bin/python
#encoding: utf-8
import os
import gtk
import sys
import gtk.gdk
import glib
import gobject
import threading

sys.path.append('..')
from oracle import *
from speak import *

(DEFAULT, SEARCHING, WAITING, RESULT) = range (0,4)
search_in_progress = 0

def show_answer ():
	set_state (RESULT)
	#try:
	print "playing"
	play_speech ('/tmp/answer')
	print 'done'
	#except:
	#	pass

def jabber_thread (q, a):
	all_files = []
	threads = []
	try:
		threads += [threading.Thread (target = download_speech, args =
			('cs', q, '/tmp/question'))]
		all_files += ['/tmp/question' ]
	except:
		pass

	for i in range (0, len(a)):
		try:
			threads += [threading.Thread (target = download_speech, args = ('cs',				"Po " + chr(ord('A')+i)+', '+a[i],
				'/tmp/answer%d' % i))]
			all_files += [ "/tmp/answer%d" %i ]
		except:
			pass
	for t in threads:
		t.start ()

	for t in threads:
		t.join ()

	for i in all_files:
		play_speech (i, wait = True)
	


def show_waiting (answer):
	print answer
	if answer is None:
		answer = "Oook?"
	answer_label.set_text (answer)
	set_state (WAITING)

def reset_gui ():
	answer_label.hide ()
	answer_img.hide ()
	thinking_img.hide ()

def set_state (state):
	if state == RESULT:

		#answer_label.show ()
		answer_evbox.show_all ()
	else:
		#answer_label.hide ()
		answer_evbox.hide_all ()

	if state == WAITING: waiting.show_all ()
	else: waiting.hide_all ()

	if state == SEARCHING: thinking_img.show () 
	else: thinking_img.hide ()

def lookup_thread (question,  options):
	try:
		answer = man_vs_machine (question, options)
		if answer is None:
			answer = "Oook?"

	except Exception as e:
		print e
		answer = "Oook!"
	
	if answer is not None:
		try:
			download_speech ("cs", answer, '/tmp/answer')
		except:
			pass
	gobject.idle_add (show_waiting, answer)

def clicked (data):
	global search_in_progress
	set_state (SEARCHING)
	q = question.get_text ()
	a = map(lambda x: x.get_text(), answers)
	if not (search_in_progress == 1):
		search_in_progress = 0
		threading.Thread(target = lookup_thread, args = (q, a)).start ()
		threading.Thread(target = jabber_thread, args = (q, a)).start ()

def waiting_clicked (sender, event_data):
	show_answer ()

def answer_clicked (sender, event_data):
	question.set_text ('')
	for i in answers:
		i.set_text ('')
	set_state (DEFAULT)


gtk.threads_init ()
background_pixbuf = gtk.gdk.pixbuf_new_from_file('images/background2.png')
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
#name = gtk.Label ('      Steve      ')
name = gtk.Label ('Micro Weaver     ')

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
fixed.put (ack, 333, 343)
ack.connect ('clicked', clicked)


# Thinking icon
thinking_img = gtk.Image ()
animation = gtk.gdk.PixbufAnimation ('images/Blue_bulb.gif')
thinking_img.set_from_animation (animation)
fixed.put (thinking_img, (640-56)/2, 70)


# "Show answer" button
waiting = gtk.EventBox ()
waiting.set_visible_window (False)
waiting_img = gtk.Image ()
waiting_img.set_from_file ('images/Blue_bulb-done2.gif')
waiting.add (waiting_img)
fixed.put (waiting, (640-56)/2, 70)
waiting.connect ('button-press-event', waiting_clicked)


# correct answer
answer_evbox = gtk.EventBox ()
answer_fixed = gtk.Fixed ()
answer_img = gtk.Image()
answer_img.set_from_file('images/answer.png')
answer_evbox.add (answer_fixed)
answer_fixed.put (answer_img, 0, 0)
answer_label = gtk.Label ()
answer_label.set_text ('kalerab')
answer_label.modify_fg (gtk.STATE_NORMAL, gtk.gdk.color_parse ('black'))
answer_fixed.put (answer_label, 25, 12)

fixed.put (answer_evbox, (640-234)/2, 110)
answer_evbox.connect('button-press-event', answer_clicked)


w.connect('destroy', gtk.main_quit)
w.show_all ()
w.fullscreen ()
set_state (DEFAULT)
gtk.main ()
