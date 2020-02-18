import music21 as m 

# The most general way to create a Chord object is by passing in a list of pitch names you want in the chord:
cMinor = m.chord.Chord(["C4","G4","E-5"])
cMinor.duration.type = 'half'
# cMinor.show()

# Since a Chord contains many pitches, it does not have a .pitch attribute, 
# but it has a pitches attribute wich returns a tuples of pitches in the chord.
print('cMinor pitches: ', cMinor.pitches)

# How you can manipulate a list, but not a tuple.
# Then in music21 will often return tuples in places where manipulating the result
#  could cause headaches or bugs down the line. 

# Play somethings:

cMajor = m.chord.Chord(["E3","C4","G4"])
cMajor.add('B4')
print('\ncMajor inversion: ', cMajor.inversion())
print('\ncMajor root: ', cMajor.root())
print('\ncMajor bass: ', cMajor.bass())
print('\ncMajor third: ', cMajor.third,' and fifth: ', cMajor.fifth, ' and seventh: ', cMajor.seventh)
cMajor.show('text')
cMajor.closedPosition().show('text')
print(cMajor.commonName)

# we can also pass a string with note names separated by spaces:
e7 = m.chord.Chord("E4 G#4 B4 D5")
e7.show('text')
print(e7.fullName)

# Like Note objects, we can put Chord objects inside a Stream
s1 = m.stream.Stream()
s1.append(cMinor)
s1.append(cMajor)
s1.append(e7)
# s1.show()

# We can mix and match Notes, Rests, and Chords:
rest1 = m.note.Rest()
rest1.quarterLength = 0.5
noteASharp = m.note.Note('A#5')
noteASharp.quarterLength = 1.5
s1.append(rest1)
s1.append(noteASharp)
s1.show()



######################   Post-tonal chords (in brief)   ####################

# There are a lot of methods for dealing with post-tonal aspects of chords.

# we will see later


#####################   NOTES CHAPTER 8  #########################
files = m.converter.Converter().subconvertersList('input')
print('Input files formats that music21 can read:')
for file in files:
    print(file)
files = m.converter.Converter().subconvertersList('output')
print('\nOutputs files formats that music21 can export:')
for file in files:
    print(file)
# Example using an url:
sBach = m.converter.parse('http://kern.ccarh.org/cgi-bin/ksdata?' +
         'l=users/craig/classical/bach/cello&file=bwv1007-01.krn&f=kern')
sBach.show()
