import music21 as m 

sBach = m.corpus.parse('bach/bwv57.8')

# Streams are hierarchical objects where the contained elements can themselves be Streams. 
# In order to get at each lower layer of the m.stream, a generator method on every m.stream called 
# recurse() will visit every element in the m.stream, starting from the beginning, 
# and if any of the subelements are also Streams, they will visit every element in that Stream. 
# Let’s create a simpler Stream to visualize what .recurse() does.

s = m.stream.Score(id='mainScore')
p0 = m.stream.Part(id='part0')
p1 = m.stream.Part(id='part1')

m01 = m.stream.Measure(number=1)
m01.append(m.note.Note('C', type="whole"))
m02 = m.stream.Measure(number=2)
m02.append(m.note.Note('D', type="whole"))
p0.append([m01, m02])

m11 = m.stream.Measure(number=1)
m11.append(m.note.Note('E', type="whole"))
m12 = m.stream.Measure(number=2)
m12.append(m.note.Note('F', type="whole"))
p1.append([m11, m12])

s.insert(0, p0)
s.insert(0, p1)
# s.show('text')

print('Using recurse() in a loop in the score')
for el in s.recurse():
    print(el.offset, el, el.activeSite)

print('\nOr filtering an aspect, .notes in this case ')
for el in s.recurse().notes:
    print(el.offset, el, el.activeSite)

# in general, .recurse() is the best way to work through all the elements of a Stream, 
# but there is another way that can be handy in some situations, and that is called .flat.
# While nested Streams offer expressive flexibility, it is often useful to be able to flatten all 
# Stream and Stream subclasses into a single Stream containing only the elements that are not Stream subclasses. 
# The flat property provides immediate access to such a flat representation of a Stream. 

print('\nPrinting flat elements of our score')
for el in s.flat:
    print(el.offset, el, el.activeSite)

# A new, temporary Stream with id of “mainScore_flat” has been created, and all of the Note objects are in there.

# Compare what .flat lets you do when looking at a larger score.
print('\nNotes in sBatch stream', len(sBach.getElementsByClass(m.note.Note)))
print('\nNotes in flat sBatch stream', len(sBach.flat.getElementsByClass(m.note.Note)) )
# of course, sBach stream contains others streams and these contain notes


# Important: Element offsets are always relative to the Stream that contains them.
# Flattening a structure of nested Streams will set new, shifted offsets for each of the elements on the Stream, 
# reflecting their appropriate position in the context of the Stream from which the flat property was accessed. 


