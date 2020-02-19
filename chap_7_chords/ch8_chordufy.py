import music21 as m 

# Chordify powerful tool for reducing a complex score with multiple parts to a succession
#  of chords in one part that represent everything that is happening in the score. 
# Take this short chorale by Bach:

b = m.corpus.parse('bwv66.6')
# b.show()

b_chords = b.chordify()
# b_chords.show()
b.insert(0, b_chords)
b.measures(0, 4).show()