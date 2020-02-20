import music21 as m 

# Chordify powerful tool for reducing a complex score with multiple parts to a succession
#  of chords in one part that represent everything that is happening in the score. 
# Take this short chorale by Bach:

b = m.corpus.parse('bwv66.6')
# b.show()

# Every note in the score is now represented in a single chord and every moment where
#  some element moves is also represented. 
b_chords = b.chordify()
# b_chords.show()

# Adding b_chords in b and showing two measures. (0 is a pickup measure)
b.insert(0, b_chords)
# b.measures(0, 1).show()
# help(m.stream.Measure.measures)

# That’s a bit messy to read, so let’s put all these chords in closedPosition
for c in b_chords.recurse().getElementsByClass('Chord'):
    c.closedPosition(forceOctave=4, inPlace=True)
# Note that when we move a chord to closed position, 
# unfortunately it loses its tie information.
# b.measures(0, 2).show()

# We can use the function roman.romanNumeralFromChord to label each of the chordified Chords:
for c in b_chords.recurse().getElementsByClass('Chord'):
    rn = m.roman.romanNumeralFromChord(c, m.key.Key('A'))
    c.addLyric(str(rn.figure))
# b.measures(0, 2).show()
# We can also just extract the lyrics, where we stored the RomanNumeral information:
for c in b_chords.measures(0,2).flat:
    if 'Chord' not in c.classes:
        continue
    print(c.lyric, end=' ')

# One great way to quickly make a reduction of a score is with chordify and 
# the annotateIntervals method on Chords. 
# Let us load up one of the most beautiful memorial pieces of all time, 
# the motet on the death of Johannes Ockeghem by Josquin des Prez (d. 1521):

o = m.corpus.parse('josquin/laDeplorationDeLaMorteDeJohannesOckeghem')
for s in o:
    print(s)
    # s.show()
# Note that we have a collection of scores with each own parts. We need to merge them.
mergedScores = o.mergeScores()
scoreExcerpt = mergedScores.measures(127, 133)
# scoreExcerpt.show()

# Let’s chordify it:
reduction = scoreExcerpt.chordify()
# reduction.show()
# We’ll iterate over the chords and put them in closed position in octave 4 and
#  run the annotateIntervals command:
for c in reduction.recurse().getElementsByClass('Chord'):
    c.closedPosition(forceOctave=4, inPlace=True)
    c.annotateIntervals()    
# reduction.show()

# We will put the reduction back into the score and show it. 
# We insert it at the zero point of the score, rather than using append because 
# it begins at the same time point as the other parts. 
# Let’s also get rid of the fourth part, since it’s blank.
scoreExcerpt.insert(0, reduction)
emptyPart = scoreExcerpt.parts[3]
scoreExcerpt.remove(emptyPart)
# scoreExcerpt.show()

#######################  Notes for chap_11 #################

# When you search metadata bundles, you can search either through every search field in 
# every metadata instance, or through a single, specific search field. 
# As we mentioned above, searching for “bach” as a composer renders different results from
#  searching for the word “bach” in general:

print("********* SEARCHING IN THE CORPUS  **************\n")

coreCorpus = m.corpus.corpora.CoreCorpus()
print(len(coreCorpus.getPaths()))
sixEight = m.corpus.search('6/8')
print(sixEight)
# b = m.corpus.search('bach')
# print(b)
# print(m.corpus.search('bach', 'title'))
# print(m.corpus.search('bach'))