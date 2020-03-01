import music21 as m21 

# Music21 has two main objects for working with keys: the KeySignature object, 
# which handles the spelling of key signatures and the Key object which does everything 
# a KeySignature object does but also knows more advanced aspects of tonal harmony.

####################### KeySignature ####################

# Now let’s get a couple of different key signatures, representing different numbers of sharps:
ks2 = m21.key.KeySignature(2)
assert ks2.sharps == 2
ks7 = m21.key.KeySignature(7)
print(ks7)
# We can get a list of which pitches are altered by the key signature with the .alteredPitches property:
print(ks2.alteredPitches)
# There’s also a method that lets us see what the accidental is for any given step:
print('C in ks2 is ', ks2.accidentalByStep('C'))
assert ks2.accidentalByStep('E') is None

# Key Signatures transpose like Pitches and Notes, taking each of the notes and moving it:
ks4 = ks2.transpose('M2')
print(ks4)
# And the number of sharps can be changed after the fact:
ks4.sharps = 0
print(ks4)

# We can get the Major or Minor scale corresponding to the Key Signature:
print(ks2.getScale('major'))
print(ks2.getScale('minor'))

# An example:
m= m21.stream.Measure()
m.insert(0, m21.meter.TimeSignature('3/4'))
m.insert(0, ks2)
d = m21.note.Note('D')
c = m21.note.Note('C')
fis = m21.note.Note('F#') # German name
m.append([d, c, fis])
# m.show()
# Note that the Note ‘C’ is treated as C-natural and thus needs the natural sign in front of it. 
# The Note F# however does not need a natural sign to be displayed.
# If we have a Measure (not just any Stream) we can also set the KeySignature for the beginning
#  of the measure with the Measure object’s .keySignature property:
m.keySignature = m21.key.KeySignature(4)
# m.show()

# Of course life isn’t all about sharps; it’d be a pretty terrible KeySignature object if 
# we couldn’t have flats. To do it, just specify the number of flats as a negative number. 
# So -1 = one flat, -2 = two flats
m.keySignature = m21.key.KeySignature(-4)
# m.show()

####################### Key ######################
# A Key is a lot like a KeySignature, but much more powerful. 
# Unlike a KeySignature, which we initialize with the number of sharps and flats, 
# we initialize a Key with a tonic string or Pitch:
kD = m21.key.Key('D')
print(kD)
kd = m21.key.Key('d')
print(kd)
# We can also make church modes:
amixy = m21.key.Key('a', 'mixolydian')
print(amixy,' that has ', amixy.sharps, ' sharps who are ', amixy.alteredPitches)
print('Transpose this in a third major we have ',amixy.transpose('M3'))
print('Keys know their .mode:' ,kd.mode, amixy.mode)
print('And their tonics are: ', kd.tonic, ' and ', amixy.tonic)
print('And the relative of ', kd, ' is ', kd.relative, ' and its parallel is ', kd.parallel)
# And because two keys are equal if their modes and tonics are the same, this is true:
assert kd.relative.relative == kd
print('It is helpuful to know that: ', kd.tonicPitchNameWithCase, ' and its relative is ',
                                                        kd.relative.tonicPitchNameWithCase)
# Some analysis routines produce keys:
bach = m21.corpus.parse('bwv66.6')
fis = bach.analyze('key')
print('The bwv66.6 key is ',  fis, ' and it has this correlation coefficient: ',
                                                 round(fis.correlationCoefficient, 3))
print('Some other keys that the Bach piece could have been in: \n', fis.alternateInterpretations[0:4])
print('Some other final keys that the Bach piece could have been in: \n', fis.alternateInterpretations[-3:])
c = bach.measures(1, 4).chordify()
for ch in c.recurse().getElementsByClass('Chord'):
    ch.closedPosition(inPlace=True, forceOctave=4)
c.show()
# So, how does it know what the key is? The key analysis routines are a variation of the famous algorithm
#  developed by Carol Krumhansl and Mark A. Schmuckler called probe-tone key finding. (used above)
# The distribution of pitches used in the piece are compared to sample distributions of pitches 
# for major and minor keys and the closest matches are reported.
# Music21 can be asked to use the sample distributions of several authors, 
# including Krumhansl and Schmuckler’s original weights:
# bach.plot('key')

# A Key object is derived from a KeySignature object and also a Scale object.
k = m21.key.Key('E-')
print('Eb key, its classes: ', k.classes)
# A few methods that are present on scales that might end up being useful for Keys as well include:
print('The 2nd degree of Eb scale is ',k.pitchFromDegree(2))
# (octaves in 4 and 5 are chosen just to give some ordering to the pitches)

#############    Key Context and Note Spelling   ##################

# Key and KeySignature objects affect how notes are spelled in some situations. 
# Let’s set up a simple situation of a F-natural whole note in D major and then B-flat minor.
s = m21.stream.Stream()
s.append(m21.key.Key('D'))
s.append(m21.note.Note('F', type='whole'))
s.append(m21.key.Key('b-', 'minor'))
s.append(m21.note.Note('F', type='whole'))
# s2 = s.makeNotation()
s.show()
# When we transpose each note up a half step (n.transpose(1)), music21 understands that the first F-natural
#  should become F-sharp, while the second one will fit better as a G-flat.
for n in s.recurse().notes:
    n.transpose(1, inPlace=True)
s.show()