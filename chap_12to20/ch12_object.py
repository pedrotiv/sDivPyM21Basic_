import music21 as m 

# Note objects, Chord objects, Stream objects, etc., are subclasses of Music21Object.
# Streams have many ways of filtering out Music21Objects (a.k.a. “elements”) according to class.
# The easiest way is with .getElementsByClass:
s= m.stream.Stream()
n= m.note.Note('A#4')
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
s.id = 'my_stream'
for element in s.getElementsByClass('Note'):
    print(element)
s.show('text')
# s.show()

# If something is a music21Object you can exploit the attributes of the object for musical purposes.print()

############  .id  #############
print(n.id)
# By default, this .id is the same as the location of the object in memory, which the built-in Python function id() returns:
print(id(n))
# But we can set it manually so that the object is easier to find later:n
n.id = 'my_note'
# This .id is especially useful for Stream objects because it will be displayed in the representation 
# of the Stream and, if there’s no other metadata, can be used as the name of the part
# Parts can be retrieved from the .parts attribute of a score by id.
bach = m.corpus.parse('bwv66.6')
sopr = bach.parts['soprano']
print(sopr)
# Other form to retieve an id is:
x= s.getElementById('my_note')
print(x, '\t', x.id)
# the similarity between music21’s .getElementById() and HTML’s .getElementById() is intentional.

############  .groups  #############
# A group is a collection of labels for an object. Think of Groups as being like .id with two differences:
#  (1) each Music21Object can have zero, one, or multiple Groups – but it has exactly one .id and 
#  (2) a single group label can belong to multiple Music21Objects.
# Groups are the equivalent of the HTML/Javascript/DOM “class”
n.groups.append('black_key')
n.groups.append('sharped')
print(n.groups)
for x in s.iter.getElementsByGroup('black_key'):
    pass 
    # x.notehead = 'circle-x'
# s.show()

############  .activeSite  #############
# A Music21Object that is inside one or more Streams should be able to get its most recently stream via its
#  .activeSite attribute. We’ve put n in s, which is called 'my_stream', so n’s .activeSite should be s.
print(n.activeSite)
# The activeSite may change over time; obviously if the note is put in another Stream then that Stream
#  will become the activeSite. Let’s put the note in a new stream, four quarter notes from the start:
t = m.stream.Stream()
t.id = 'new_stream'
t.insert(4.0, n)
print(n.activeSite)
# t.show()
# We can also change the activeSite since, of course, it belong to the stream.
n.activeSite= s

############  .offset  #############
# The .offset of a Music21Object is the number of quarter notes from the start of the Stream it is a part of. 
# If we change the offset of the Note it changes it in the Stream, so that if we change the activeSite
#  away and back, the offset is preserved.
n.activeSite = s
n.offset = 2.0
n.activeSite = t
n.activeSite = s
print(n.offset)
n2 = m.note.Note('G-2')
n2.offset = 20.0
s.insert(n2)
n2.activeSite
s.show()

############  .priority  #############
# If you have a sream with two or more elements at the same offset, priority, as a integer number line,
# fix the order who one comes first. Default is zero, negative is first to positive is last.

############  .classSortOrder  #############
# Objects seem to be sorted by offset first, then priority, then when they were inserted. But what about this:
tc = m.clef.TrebleClef()
s.insert(0.0, tc)
s.show('text')
print(tc.priority, n.priority, n2.priority)
# It’s because there is another property that aids in sorting, and that is called .classSortOrder. 
print(tc.classSortOrder, n.classSortOrder, n2.classSortOrder)
# any change in .classSortOrder applied to the class changes it for all its members