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
	shortestNoun = ''
	for lemma in lemmas:
		if lemma[-1] == 'V' and lemma[-4] == 'a':
			hasVerbOfFirst = True
			return [lemma]

		elif lemma[-1] == 'N':
			if shortestNoun == '' or len(lemma) < len(shortestNoun):
				shortestNoun = lemma

	for lemma in lemmas:
		if lemma[-1] == 'A' or lemma[-1] == 'N':
			continue

		newLemmas.append(lemma)		

	if len(shortestNoun) > 0:
		newLemmas.append(shortestNoun)

	return newLemmasdef runXCut(lemmas):newLemmas = []
	hasX = False
	for lemma in lemmas:
		parts = lemma.split('+')
		word = parts[0]
		if len(parts) > 2:
	newLemmas.append(word + '+' + parts[2])
	return newLemmas


def printWordLemmas(word, lemmas):
	print str(word) + '\t' + '\t'.join(lemmas)

def analizeWordLemmas(word, lemmas):
	newLemmas = runXCut(lemmas)
	if len(newLemmas) == 0:
		newLemmas = runLemmasHeuristics(lemmas)
	else:
		newLemmas = runLemmasHeuristics(newLemmas)
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