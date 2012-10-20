#!/usr/bin/python

# usage example: cat temporary.prediction.raw.result | head -n100 | python py/cut_lemmas.py

import codecs
import json

import itertools
import operator

import re
import sys

def from_stdin(encoding = 'utf-8'):
    iterable = codecs.getreader(encoding)(sys.stdin)
    for item in iterable:
        yield item.rstrip('\r\n')

def analizeWordLemmas(word, lemmas):
	lemmasDict = {}
	for lemma in lemmas:
		parts = lemma.split('+')
		lemmasDict[parts[0]] = set(map(str, parts[1:]))
	print lemmasDict
	print '=================================================='
	#print "got word %s with %d lemmas" % (word, len(lemmas))

tempWord = ''
tempLemmas = []
for line in from_stdin():
	if len(line) == 0:
		analizeWordLemmas(tempWord, tempLemmas)
		tempWord = ''
		tempLemmas = []
		continue

	words = line.split('\t')
	tempWord = words[0]
	tempLemmas.append(words[1])

if tempWord != '':
	analizeWordLemmas(tempWord, tempLemmas)