#!/usr/bin/env python3

"""
Author:	James Boivie
Date: 	2016-05-02
"""

import random
from nltk.corpus import brown
import ngram
import re
import sys


def load_model(name='wordSet', sents=None):
	if name != 'wordSet':
		wordSet = name + 'Dict.txt'
		if not sents:
			try:
				with open(name + '.txt', 'r', encoding='latin-1') as f:
					sents = [re.sub("[^\w ]", "", line.lower()).split() for line in f if not line.isspace()]
			except FileNotFoundError as e:
				print(e)
				exit(1)
	else:
		wordSet = 'wordSet.txt'
		sents = brown.sents()

	ngram_model = ngram.Model(sents)

	return ngram_model, wordSet

def grabWordTags(word, elim=False):
    ftags = []
    with open(wordSet, 'r', encoding='latin-1') as f:
        for line in f:
            tags = line.split()
            if (tags[0] == word):
                if (elim):
                    for tag in tags:
                        for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                            tag = tag.replace(i, '')
                        ftags.append(tag)
                    return ftags[1:]
                return tags[1:]

def findSound2(wordTags):
    key = []
    for i in range(len(wordTags)):
        key.append(wordTags[len(wordTags)-1-i])
        if (len(wordTags[len(wordTags)-1-i]) == 3):
            return key
    return key

def findVowelSounds(tags):
    vTags = []
    for tag in tags:
        if (len(tag) == 3):
            vTags.append(tag)
    return vTags

def getRhyme2(sounds, syl=None):
    rhymes = []
    sounds2 = []
    for i in range(len(sounds)):
        for j in ['0','1','2','3','4','5','6','7','8','9']:
            sounds[i] = sounds[i].replace(j,'')
    with open(wordSet, 'r', encoding='latin-1') as f:
        for line in f:
            tags = line.split()
            vSound = len(findVowelSounds(tags))
            for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                line = line.replace(i, '') 
            tags = line.split()
            i = 0 
            for sound in sounds:
                i = i - 1 
                if (sound != tags[i]):
                    break
                if ((i * -1) == len(sounds)):
                    if ((syl == None) or (vSound == syl)):
                        rhymes.append(tags[0]) 
    return rhymes

def matches(stresses, vTags):
    for i in range(len(stresses)):
        if ((stresses[i] == 1) and ((vTags[i][2] == '1') or (vTags[i][2] == '2'))):
            continue
        if ((stresses[i] == 0) and (vTags[i][2] == '0')):
            continue
        return False
    return True 

def findWords(stresses):
    words = []
    with open(wordSet, 'r', encoding='latin-1') as f:
        for line in f:
            tags = line.split()
            vTags = findVowelSounds(tags[1:])
            if (len(vTags) == len(stresses)):
                if (matches(stresses, vTags)):
                    words.append(tags[0]) 
    return words

def mam(start, length):
    array = []
    i = 0
    while i < length:
        array.append(start)
        start = 1 - start
        i += 1
    return array

def line(stresses, low=1,high=4):
    sentence = []
    i = 0
    while (i < len(stresses)):
        wl = random.randint(low,high)
        if ((i + wl) > len(stresses)):
            wl = len(stresses) - i
        words = findWords(stresses[i:(i+wl)])
        if (len(words) == 0):
            continue
        for j in range(len(words)):
            if (words[j][-1] == ')'):
                words[j] = words[j][:-3]
        # CODE TO CHOOSE WORD MAY CHANGE
        # Previous word is at sentence[-1]
        if len(sentence) > 0:
            word = ngram_model.choose_weighted_random([sentence[-1]], words)
        else:
            word = random.choice(words)
        
        sentence.append(word)
        if (i == 0):
            pass            
        i += wl
    return sentence

def magicFinder(wordToRhyme, oldWord):
    tags = grabWordTags(wordToRhyme)
    tags2 = grabWordTags(oldWord)
    syl = len(findVowelSounds(tags2))
    sounds = findSound2(tags)
    rhymes = getRhyme2(sounds, syl)
    if (len(rhymes) == 0):
        return [oldWord]
    return rhymes

def testLimerick4():
    line1 = line([0,1,0,0,1,0,0,0,1])
    print('20%')
    line2 = line([0,1,0,0,1,0,0,0,1])
    line2[-1] = random.choice(magicFinder(line1[-1], line2[-1]))
    print('40%')
    line5 = line([0,1,0,0,1,0,0,0,1])
    line5[-1] = random.choice(magicFinder(line1[-1], line5[-1]))
    print('60%')
    line3 = line([0,1,0,0,0,1])
    print('80%')
    line4 = line([0,1,0,0,0,1])
    line4[-1] = random.choice(magicFinder(line3[-1], line4[-1]))
    print('100%')
    print(line1)
    print(line2)
    print(line3)
    print(line4)
    print(line5)

def testLimerick3():
    line1 = line([0,1,0,0,1,0,0,0,1])
    print('20%')
    line2 = line([0,1,0,0,0,1,0,0,1])
    line2[-1] = random.choice(magicFinder(line1[-1], line2[-1]))
    print('40%')
    line5 = line([0,1,0,0,1,0,0,0,1])
    line5[-1] = random.choice(magicFinder(line1[-1], line5[-1]))
    print('60%')
    line3 = line([0,1,0,0,0,1])
    print('80%')
    line4 = line([0,1,0,0,0,1])
    line4[-1] = random.choice(magicFinder(line3[-1], line4[-1]))
    print('100%')
    print(line1)
    print(line2)
    print(line3)
    print(line4)
    print(line5)

def testLimerick2():
    line1 = line([0,0,1,0,0,1,0,0,1])
    print('20%')
    line2 = line([0,0,1,0,0,1,0,0,1])
    line2[-1] = random.choice(magicFinder(line1[-1], line2[-1]))
    print('40%')
    line5 = line([0,0,1,0,0,1,0,0,1])
    line5[-1] = random.choice(magicFinder(line1[-1], line5[-1]))
    print('60%')
    line3 = line([0,0,1,0,0,1])
    print('80%')
    line4 = line([0,0,1,0,0,1])
    line4[-1] = random.choice(magicFinder(line3[-1], line4[-1]))
    print('100%')
    print(line1)
    print(line2)
    print(line3)
    print(line4)
    print(line5)

def testLimerick1():
    line1 = line([0,1,0,0,1,0,0,1,0])
    print('20%')
    line2 = line([0,1,0,0,1,0,0,1,0])
    print('40%')
    line5 = line([0,1,0,0,1,0,0,1,0])
    print('60%')
    line3 = line([0,1,0,0,1,0])
    print('80%')
    line4 = line([0,1,0,0,1,0])
    print('100%')
    print(line1)
    print(line2)
    print(line3)
    print(line4)
    print(line5)

def testIambic():
    sentence = []
    i = 0
    while (i < 10):
        wl = random.randint(1,3)
        if ((i + wl) > 10):
            wl = 10 - i
        if ((i % 2) == 0):
            arr = mam(0, wl)
        else:
            arr = mam(1, wl)
        words = findWords(arr)
        for j in range(len(words)):
            if (words[j][-1] == ')'):
                words[j] = words[j][:-3]
        if len(sentence) > 0:
            word = ngram_model.choose_weighted_random([sentence[-1]], words)
        else:
            word = random.choice(words)
        sentence.append(word)
        i += wl
    return sentence

def testCouplet():
    sentence = []
    for i in range(20):
        sentence.append(testIambic())
        if ((i % 4) > 1):
            sentence[i][-1] = random.choice(magicFinder(sentence[i-2][-1], sentence[i][-1]))
        print(str((i+1)*5) + "%")
    for i in range(20):
        print(sentence[i])

def randomSyllable(num):
    arr = []
    for i in range(num):
        arr.append(random.randint(0,1))
    return arr

def testHaiku():
    line1 = line(randomSyllable(5))
    print('33%')
    line2 = line(randomSyllable(7))
    print('67%')
    line3 = line(randomSyllable(5))
    print('100%')
    print(line1)
    print(line2)
    print(line3)

def testRhyme(word):
    tags = grabWordTags(word)
    sounds = findSound2(tags)
    rhymes = getRhyme2(sounds)
    return rhymes



########
##MAIN##
########
if len(sys.argv) > 1:
	ngram_model, wordSet = load_model(sys.argv[1])
else:
	ngram_model, wordSet = load_model()

last = 'h'
while 1:
	try:
		command = input("Give a command: ")
		if command == '':
			command = last
		else:
			last = command
		if command == 'h':
			print("(l)imerick, (i)ambic pentameter, (c)ouplet, hai(k)u, (h)elp")
		if command == 'l':
			testLimerick4()
		elif command == 'i':
			print(testIambic())
		elif command == 'c':
			testCouplet()
		elif command == 'k':
			testHaiku()
		elif command == 'q':
			exit(0)
	except EOFError:
		print()
		exit(0)
