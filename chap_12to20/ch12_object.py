import music21 as m 

# Note objects, Chord objects, Stream objects, etc., are subclasses of Music21Object.
# Streams have many ways of filtering out Music21Objects (a.k.a. “elements”) according to class.
# The easiest way is with .getElementsByClass:
s= m.stream.Stream()
n= m.note.Note('A-4')
n.quarterLength = 4
r= m.note.Rest()
s.append(m.clef.TrebleClef())
s.append(m.meter.TimeSignature('3/4'))
s.append(m.note.Note("A"))
s.append(m.note.Rest())
s.append(m.note.Note("B"))
s.append(r)
s.append(m.note.Note('B-3'))
s.append(n)
for element in s.getElementsByClass('Note'):
    print(element)
s.show('text')
s.show()

