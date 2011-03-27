#!/usr/bin/python
# vim: ts=2:sts=2:sw=2:et
import urllib
import simplejson
import pprint
import re;
import socket;

socket.setdefaulttimeout(5)

class MyOpener(urllib.FancyURLopener):
  version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'


# Takes slovak text and translates it into english
#
#Read more: http://www.halotis.com/2009/09/15/google-translate-api-python-script/#ixzz1FSJPg1Q6 
def translate(text):
  print text;
  src = 'sk';
  to = 'en';
  params = ({'langpair' : '%s|%s' % (src, to), 'v': '1.0', 'q' : text})
  baseUrl = "http://ajax.googleapis.com/ajax/services/language/translate"
  resp = simplejson.load(urllib.urlopen('%s' % (baseUrl), data = urllib.urlencode(params)))
  return resp['responseData']['translatedText']


## Fetch results from google search api
def fetch_results(query):
  print "Fetch Results", query
  query = urllib.urlencode({'q' : query})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % (query)
  search_results = urllib.urlopen(url)
  json = simplejson.loads(search_results.read())
  return json['responseData'];


# Fetch the number of results
# Warning: don't use data['cursor']['estimatedResultCount']
# as it greatly varies from google search results
# and I suspect that it is somewhat random and bad
def number_of_results(data):
  __search_url = data['cursor']['moreResultsUrl']
  opener = MyOpener(); # Custom opener needed
  f = opener.open(__search_url);
  result_count = 0;
  for line in f:
    m = re.search("About ([,0-9]+) results", line)
    if m:
      result_count = int(m.groups(1)[0].replace(",", ""));
  return result_count


## Estimate score signals for question and choice
def estimate_scores(question, choices):
  print "------------- Estimating hits for -- ", question, "--", choices
  signals = {};

  for choice in choices:
    choiceEN = choices[choice]
    signals[choice] = {
        'result_count' : 0,
        'results_relative' : 0,
        'title_count' : 0,
        'content_count':0,
        'in_results_count' : 0};
    query = question + ' "' + choiceEN + '"'
    data = fetch_results(query);
    signals[choice]['result_count'] = number_of_results(data);


  ## Try to estimate metrics for original query search
  results_orig = fetch_results(question)
  base_result_count = number_of_results(results_orig)
  for i in results_orig['results']:
    for choice in choices:
      choiceEN = choices[choice]
      signals[choice]['results_relative'] = 1.0 * signals[choice]['result_count'] / base_result_count
      if i['title'].find(choiceEN) != -1:
        signals[choice]['title_count'] += 1;
      if i['content'].find(choice) != -1:
        signals[choice]['content_count'] += 1

  print "going through results..."
  ## Estimate metrics for original query result pages
  for i in results_orig['results']:
    try:
      print "Result : ", i['url']
      for line in urllib.urlopen(i['url']):
        for choice in choices:
          choiceEN = choices[choice]
          if line.find(choiceEN) != -1:
            signals[choice]['in_results_count'] += 1;
    except:
      print "Failed fetching", i['url']
      pass

  return signals

#otazka = "Kedy zacala prva svetova vojna"
#odpovede = ["1914", "1915", "1916", "1918"]

#otazka = "Kto je sucasny prezident USA?";
#odpovede = ["Barack Obama", "Thomas Jefferson", "Lady Gaga", "George Washington"]

#otazka = "Kolko noh ma pavuk?"
#odpovede = ["dve", "styri", "sest", "osem"]

#otazka = "Ake je hlavne mesto Australie?"
#odpovede = ["Sydney", "Canberra", "Melbourne", "Adelaide"]

#otazka = "Kto je autorom knihy hobit?"
#odpovede = ["J.R.R Tolkien", "Terry Pratchett", "Clean Water", "John End"]

#otazka = "Ktora krajina ma najvacsiu rozlohu?"
#odpovede = ["Cina", "Rusko", "Kanada", "Slovensko"]


#otazka=raw_input("Zadaj svoju otazku:")
#print "zadaj svoje odpovede kazdu na riadok, za poslednou daj enter"
#odpovede = []
#while True:
#  odp=raw_input("Zadaj odpoved:")
#  if odp:
#    odpovede.append(odp)
#  else:
#    break;

def vyhodnot(data):
  res = []
  for key, value in data.iteritems():
    score = value['in_results_count'] + value['results_relative'] / 2.0 + \
        value['content_count'] * 10 + value['title_count'] * 10;

    res.append((score, value, key))
  res.sort();
  res.reverse();
  for x in res:
    print "-----------------"
    print x[2], x[0], x[1]
  return res

