#!/usr/bin/python
#encoding:utf-8
import urllib
import httplib
import re
import os

class MyOpener(urllib.URLopener):
  version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def download_speech(lang, text, filename):
  print "Fetching speach..."
  text = re.sub(' +', ', ', text)
  baseUrl = "http://translate.google.com/translate_tts?"
  params = ({'tl' : lang, 'q' : text})
  os.system("rm '%s'" %filename);
  stream = MyOpener().retrieve(baseUrl + urllib.urlencode(params),
        filename)
  print "Done"


def play_speech(filename):
  os.system("mplayer '%s'" % filename)

download_speach('sk', "Najvyšším vrchom Južnej Ameriky je:", "/tmp/question.mp3");
download_speach('sk', "a, Ojos del Salado", "/tmp/answer_a.mp3");

play_speach("/tmp/question.mp3");
play_speach("/tmp/answer_a.mp3");

