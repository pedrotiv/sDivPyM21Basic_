import music21 as m 

n= m.note.Note('A-2', type= 'half')
s= m.stream.Stream()
s.insert(0, n)
# s.show('text')

# Note objects, Chord objects, Stream objects, etc., are subclasses of Music21Object.

