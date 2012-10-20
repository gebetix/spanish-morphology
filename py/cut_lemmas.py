#!/usr/bin/python

import codecs
import re
import sys

def from_stdin():
    iterable = codecs.getreader('utf-8')(sys.stdin)
    for item in iterable:
        yield item.rstrip('\r\n').encode('utf-8')

def runLemmasHeuristics(lemmas):
	newLemmas = []
	hasVerbOfFirst = False
	for lemma in lemmas:
		if lemma[-1] == 'V' and lemma[-4] == 'a':
			hasVerbOfFirst = True
			return [lemma]

	for lemma in lemmas:
		if lemma[-1] == 'A':
			continue

		newLemmas.append(lemma)		

	return newLemmas

def printWordLemmas(word, lemmas):
	print str(word) + '\t' + '\t'.join(lemmas)

def analizeWordLemmas(word, lemmas):
	newLemmas = runLemmasHeuristics(lemmas)
	printWordLemmas(word, newLemmas)

firstWordMode = True
tempWord = ''
tempLemmas = []
for line in from_stdin():
	words   = line.split('\t')
	newWord = words[0]
	lemma   = words[1]

	if firstWordMode:
		tempWord = newWord
		firstWordMode = False

	if newWord == tempWord:
		tempLemmas.append(lemma)
	else:
		analizeWordLemmas(tempWord, tempLemmas)
		tempWord   = newWord
		tempLemmas = [lemma]


if tempWord != '':
	analizeWordLemmas(tempWord, tempLemmas)