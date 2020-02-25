import  music21 as m21 

# At this point you know how to find a Music21Object, how to name them and group them (with .id and .groups)
#  and how to position them in Streams (with .offset, .priority, .classSortOrder and the .activeSite)

###########   .sites   ############
# All Music21Objects have a .sites property which is a Sites object which holds information 
# about all the places the Music21Object is stored in. 

n = m21.note.Note()
s1 = m21.stream.Stream(id='s1')
s2 = m21.stream.Stream(id='s2')
s1.insert(10, n)
s2.insert(20, n)
for s in n.sites:
    print(s, s.elementOffset(n))
# Note that the order of the Streams in .sites is guaranteed to be the order in which the note was inserted into the site.
# There’s a lot more that .sites can do, but primarily for developers. We will get back to sites later.

###########   .derivation   ############
# A Derivation object is a pointer to an object that this object is derived from in some way. 
# They’ve gone their separate ways to an extent, but may want to talk to each other later.
c = m21.note.Note("C4")
print('derivation of c note:', c.derivation)
# but if we create a new note from c note:
f = c.transpose('P4')
print('derivation of f note:', f.derivation)
# We can add a sharp to C and the transpose relationship of F to C does not affect it:
c.pitch.accidental = m21.pitch.Accidental('sharp')
print(c, f)
# But if f wants to do something to c, it can by changing itself and every element of its .derivation.chain():
f.notehead = 'diamond'
for n in f.derivation.chain():
    n.notehead = 'diamond'
print(f.notehead, c.notehead)
# While f can search upwards in its .derivation.chain() and find c, c cannot find f in its derivation; 
# it is a connection that is designed to be one-way only.

##########################   CONTEXT ATTRIBUTES   ########################

# Several attributes of Music21Objects only work after the object has been placed inside a Stream 
# that has certain features of their own.

###########   .measureNumber   ############
# An easy one to understand is .measureNumber which finds the .number value of the measure 
# that an object is placed in:
n = m21.note.Note('C')
m = m21.stream.Measure()
m.number = 7
m.append(n)
print(n.measureNumber)
# This works even if a note is inside a voice inside a measure:
v = m21.stream.Voice()
n2 = m21.note.Note('D')
v.append(n2)
m.insert(0, v)
print(n2.measureNumber)
# Without a context, you’ll get None
n3 = m21.note.Note()
print(n3.measureNumber is None)

###########   .seconds   ############
# The secondes attribute requires a tempo.MetronomeMark() to be placed into the Stream before
#  the object and will calculate how many seconds the object (note, etc.) lasts at that tempo:
m.insert(0, m21.tempo.MetronomeMark('Allegro', 120))
print ('Note n quarterLength: ',n.quarterLength,' and secondes: ', n.seconds)
# Unlike .measureNumber and the rest of the attributes we will see below, you can change .seconds 
# to reflect exact timing you might have from audio or MIDI data.
n.seconds = 0.6
print(n.seconds)
# An object with no tempo information in its surrounding context returns an error for .seconds
# So use try...except... to catch this:
for el in (n, n2, n3):
    seconds = "No information"
    try:
        seconds = el.seconds
    except m21.exceptions21.Music21Exception:
        pass
    print(el.step, seconds)
# The last three context attributes, .beat, .beatStr (beat string), and .beatStrength, all require 
# TimeSignature contexts. Since they’re the topic of our next chapter we’ll put them off until then.

##########################   METHODS   ########################

###########   .getOffsetBySite() and .setOffsetBySite()   ############
# These methods work as the .offset attribute but can work on any site where the object is a part of.
s1 = m21.stream.Stream(id="s1")
s1.insert(10, n)
s2 = m21.stream.Stream(id="s2")
s2.insert(20, n)
print(n.getOffsetBySite(s1))
n.setOffsetBySite(s1, 15.0)
print(n.getOffsetBySite(s1))
print(n.getOffsetBySite(s2))

###########   .getContextByClass()   ############
# This is an extremely powerful tool – you might not use it often, but be assured that music21 is using 
# it on your behalf all the time when sophisticated analysis is involved. 
# It finds the active element matching a certain class preceeding the element. 
# Let me demonstrate:
bach = m21.corpus.parse('bwv66.6')
lastNote = bach.recurse().getElementsByClass('Note')[-1]
print('Last note of BWV66.6: ', lastNote)
print('Where part is: ', lastNote.getContextByClass('Part'))
print('and the key at that moment is: ', lastNote.getContextByClass('KeySignature'))
print('and the time at that moment is: ', lastNote.getContextByClass('TimeSignature'))
# Other example:
gloria = m21.corpus.parse('luca/gloria')
soprano = gloria.parts[0]
lastTimeSignature = None
for n in soprano.recurse().getElementsByClass('Note'):
    thisTimeSignature = n.getContextByClass('TimeSignature')
    if thisTimeSignature is not lastTimeSignature:
        lastTimeSignature = thisTimeSignature
        print('Gloria de Luca, TimeSignature:',thisTimeSignature,' at measure: ', n.measureNumber)
# Internally .getContextByClass uses another Music21Object method called .contextSites() which is 
# a generator that tells the system where to search next:
print('\nExploring contextSites method: (see line 102)')
for cs in lastNote.contextSites():
    print(cs)
# .contextSites returns a “ContextTuple” which is a lightweight namedtuple that has three attributes, 
# site, offset, and recurseType.
# The first ContextTuple says that first the elements, of site Measure 9, should be searched beginning at
# offset 2.0 and (because recurseType is elementsFirst) working backwards to the beginning of the measure, 
# then if the matching context isn’t found, the measure will be flattened 
# (in case there are other voices in the measure) and anything from before offset 2.0 of that flattened stream
#  will be searched.
# If that fails, then the Bass part as a whole will be searched, with all elements flattened, 
# beginning at offset 35 and working backwards. That way if the context is in another measure it will be found.
# Then if that fails, it will look at the score as a whole, beginning at offset 35 and working backwards,
# but only looking at things that are at the score level, not looking at elements within other parts. 
# There may be scores where for instance, expressive markings appear at the Score level. This will find them.

###########   Splitting methods   ############
# There are three methods to split an object:
# .splitAtQuarterLength() – splits an object into two objects at the given quarter length
# .splitByQuarterLengths() – splits an object into two or more objects according to a list of quarter lengths
# .splitAtDurations() – takes an object with a complex duration (such as 5.0 quarters) and 
# splits it into notatable units.
n = m21.note.Note('C#5')
n.duration.type = 'whole'
n.articulations = [m21.articulations.Staccato(), m21.articulations.Accent()]
n.lyric = 'hi!'
n.expressions = [m21.expressions.Mordent(), m21.expressions.Trill(), m21.expressions.Fermata()]
# n.show()
# Now let’s split this note just before beat 4:
splitTuple = n.splitAtQuarterLength(3)
s3 = m21.stream.Stream()
s3.append(splitTuple)
# s3.show()
# Notice the choices that music21 made – the two notes are tied, the lyrics are sung at the beginning, 
# the accent and mordent appear at the beginning of the note while the staccato and fermata(!) appear 
# on the second note, while trill mark gets put onto the first note only.
# This is part of the “batteries included” music21 approach – try to do something musically smart in most cases. 
# In fact, it’s even a bit smarter – the splitTuple knows that there’s something called a TrillExtension spanner in
# it which should be put into the Stream:
for thisSpanner in splitTuple.spannerList:
    s3.insert(0, thisSpanner)
s3.show()










    