#!/usr/bin/env python3

import ngram
import nltk
from nltk.corpus import brown

model = ngram.Model(brown.sents())


wordlist = ['the','he','she','we','any']
badwordlist = ['thdsafjasjfsaf','asdfasd']

print("\nMax:")
print(model.choose_max(['then'], badwordlist))
for i in range(3):
	print(model.choose_max(['then'], wordlist))

print("\nWeighted:")
print(model.choose_weighted_random(['then'],badwordlist))
for i in range(0,10):
	print(model.choose_weighted_random(['then'],wordlist))

print("\nTrue random")
print(model.choose_random(['then'], badwordlist))
for i in range(0,10):
	print(model.choose_random(['then'],wordlist))
