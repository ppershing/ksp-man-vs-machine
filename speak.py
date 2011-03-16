#!/usr/bin/python
#encoding:utf-8
import urllib
import httplib
import re
import os

class MyOpener(urllib.URLopener):
  version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def speak(lang, text):
  text = re.sub(' +', ', ', text)
  baseUrl = "http://translate.google.com/translate_tts?"
  params = ({'tl' : lang, 'q' : text})
  stream = MyOpener().retrieve(baseUrl + urllib.urlencode(params),
        "/tmp/speak.mp3")
  os.system("mplayer /tmp/speak.mp3");
  

speak('sk', "Najvyšším vrchom Južnej Ameriky je:");
speak('sk', "a, Ojos del Salado");


