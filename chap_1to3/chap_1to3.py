import music21 as m21

a = m21.note.Note("F#5")
#a.show()
print(a)

b = m21.note.Note("A4")
print(b)

print(b.pitch.frequency)

# same result is Duration(2) because the quarter is equal 1
d = m21.duration.Duration('half') 
print(d.quarterLength)

b.duration = d
print(b.duration.type)

a.duration.quarterLength = 3
print("a quarterLength =", a.duration.quarterLength)
print("a type =", a.duration.type)
print("a dots =", a.duration.dots)

a.show('lily')

