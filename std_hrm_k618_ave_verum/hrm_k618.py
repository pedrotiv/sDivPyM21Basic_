import music21 as m21 

'''
Studies of Mozart Ave Verum K618
Next:   We find each modulations and we adjust the rn variable to its
        Delete unused lines.
'''

b = m21.corpus.parse('k618')
# b.show()
b_chords = b.chordify()
# b_chords.show()
# Adding b_chords in b. (0 is a pickup measure)
# b.show()
# let’s put all these chords in closedPosition
for c in b_chords.recurse().getElementsByClass('Chord'):
    # c.closedPosition(forceOctave=4, inPlace=True)
    # c.annotateIntervals()    
    pass
# b.show()
# b_chords.show()
# We can use the function roman.romanNumeralFromChord to label each of the chordified Chords:
for c in b_chords.recurse().getElementsByClass('Chord'):
    rn = m21.roman.romanNumeralFromChord(c, m21.key.Key('D'))
    c.addLyric(str(rn.figure))
# We can also just extract the lyrics, where we stored the RomanNumeral information:
# for c in b_chords.measures(0,2).flat:
#     if 'Chord' not in c.classes:
#         continue
#     print(c.lyric, end=' ')
b.insert(0, b_chords)
b.show()

