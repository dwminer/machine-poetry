#!/usr/bin/env python3

g = open('formattedLyrics.txt', 'w', encoding='latin-1')
words = set()
with open('toolLyrics.txt', 'r', encoding='latin-1') as f:
    for line in f:
        line = line.replace(',','')
        line = line.replace('.','')
        line = line.replace('"','')
        line = line.replace(':','')
        line = line.replace(';','')
        line = line.replace('-','')
        for tag in line.split():
            words.add(tag.upper())
            #g.write(tag.upper()+'\n')
with open('wordSet.txt', 'r', encoding='latin-1') as h:
    for line in h:
        tags = line.split()
        if (tags[0] in words):
            g.write(line)
        else:
            vTags = []
            for tag in tags[1:]:
                if (len(tag) == 3):
                    vTags.append(tag)
            if (len(vTags) == 1):
                if (vTags[0][2] == '0'):
                    g.write(line)
g.close()       
