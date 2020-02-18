import music21 as m21 
# The Stream object and its subclasses (Score, Part, Measure) are the fundamental containers 
# for music21 objects such as Note, Chord, Clef, TimeSignature objects.
# A container is like a Python list.
# A critical feature of music21’s design that distinguishes it from other music analysis frameworks
#  is that one music21 object can be simultaneously stored (or, more accurately, "referenced")
#  in more than one Stream. 
# Go to work:

s1 = m21.stream.Stream()
n1 = m21.note.Note("D#5")
# This creates independent copies (using Python’s copy.deepcopy function), not references.
s1.repeatAppend(n1,4)
# Print the offset and the object, respectively
s1.show('text')
# s1.show()

for note in s1:
    print('The note is a: ', note.name)

note1 = m21.note.Note("C4")
note1.duration.type = 'half'
note2 = m21.note.Note("F#4")
note3 = m21.note.Note("B-2")

stream1 = m21.stream.Stream()
stream1.id = 'some notes'
stream1.append(note1)
stream1.append(note2)
stream1.append(note3)

biggerStream = m21.stream.Stream()
note2 = m21.note.Note("D#5")
biggerStream.insert(0, note2)
biggerStream.append(stream1)

biggerStream.show('text')
biggerStream.show()

# help(m21.note.Note)