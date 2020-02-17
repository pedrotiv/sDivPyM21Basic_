import music21 as m21

n1 = m21.note.Note("F#5")
#n1.show()
print(n1)

n2 = m21.note.Note()
print(n2)

print(n2.pitch.frequency)

# same result is Duration(2) because the quarter is equal 1
d = m21.duration.Duration('half') 
print(d.quarterLength)

n2.duration = d
print(n2.duration.type)

n1.duration.quarterLength = 1
print("n1 quarterLength =", n1.duration.quarterLength)
print("n1 type =", n1.duration.type)
print("n1 dots =", n1.duration.dots)

# n1.show('lily')
# n2.show('lily')

n1.pitch.nameWithOctave = 'E-5'
n1.duration.quarterLength = 3.0

# n1.show('lily')

n3 = m21.note.Note("F6")
# n3.lyric = "I'm the Queen of the Night!"

# n3.show('lily')

# Now we’ll add as a lyric the name of the note itself and its pitchClassString.
n1.quarterLength = 6.25
n1.addLyric(n1.nameWithOctave)
n1.addLyric('Class: %s' % n1.pitch.pitchClassString)
n1.addLyric('ql: %s' % n1.quarterLength)
n1.show('lily')




