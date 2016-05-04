#!/usr/bin/env python3
from __future__ import division

import nltk
from nltk.corpus import brown
import random, itertools, bisect

class Model:
	def __init__(self, sents, n=2, cpd_class=nltk.MLEProbDist):
		self.debug = True
		self.N   = n
		self.CPD_CLASS = cpd_class
		self.cfd = nltk.ConditionalFreqDist()
		self.fd  = nltk.FreqDist()

		# filter out punctuation and convert to lowercase
		sents = (list(map(str.lower, filter(str.isalpha, sent))) for sent in sents)

		for sent in sents:
			for word in sent:
				self.fd[word] += 1
			for ngram in zip( *[ sent[i:] for i in range(self.N)]):
				self.cfd[ngram[:-1]][ngram[-1]] += 1

		# Calculate conditional probabilities.
		self.cpd = nltk.ConditionalProbDist( self.cfd,
		                                     self.CPD_CLASS,
		                                     bins=self.fd.B() )

	# The choose_ methods all follow the same form:
	# prev: A list of the previous n-1 words that were chosen (e.g. 1 for a bigram model)
	# wordlist: A list of words to choose from
	
	# Deterministically chooses the most probable word from wordlist based on the model
	def choose_max(self, prev, wordlist):
		prev = tuple([w.lower() for w in prev])
		prob, choice = max((self.cpd[prev].prob(w.lower()), w) for w in wordlist)
		if self.debug:
			print("Returning {} (probability {}%)".format(choice, 100 * prob))
		return choice


	# Randomly chooses a word from wordlist weighted by their likelihood in the model
	def choose_weighted_random(self, prev, wordlist):
		prev = tuple([w.lower() for w in prev])
		choices, weights = zip(*((w, self.cpd[prev].prob(w.lower())) for w in wordlist))
		cumulative_dist = list(itertools.accumulate(weights))
		x = random.random() * cumulative_dist[-1]
		if max(weights) > 0:
			choice = choices[bisect.bisect(cumulative_dist, x)]
			if self.debug:
				print("Returning {} (probability {}%) from {}, prev={}".format(
				                                               choice,
				                                               100 * self.cpd[prev].prob(choice.lower()),
				                                               len(choices),
				                                               prev))
			return choice
		else:
			choice = random.choice(wordlist)
			if self.debug:
				print("Randomly returning a word from {}, prev={}".format(len(wordlist), prev))
			return choice
	
	# Chooses a word from wordlist completely randomly, excepting words not in the dictionary (unless we've no other choice)
	def choose_random(self, prev, wordlist):
		prev = tuple(prev)
		choices = [w for w in wordlist if self.cpd[prev].prob(w.lower()) > 0]
		if not len(choices) > 0:
			choices = wordlist
		return random.choice(choices)
