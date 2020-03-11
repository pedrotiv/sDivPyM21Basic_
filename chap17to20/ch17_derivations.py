import music21 as m21

'''
What we�ve seen already is that iterating over the score via, 
for n in score: print n will only get you the highest level of objects,
 namely the Metadata object and the two Part objects. 
The inner objects, measures, clefs, notes, etc. Will not be available. 
The simplest way of getting at all these objects is with the
 Stream.flat property. Calling it on this score will change the 
representation so that only the non-stream elements remain in the score.
This section explains the relationship between the original stream.
Score object, which we will call s, and the flat representation,
 which we will call s.flat or sf. The relationship between the two 
is called a Derivation.
'''

s = m21.corpus.parse('mozart/k80', 1)
s.id = 'mozartK80'
# print(s.derivation)
# <Derivation of <music21.stream.Score mozartK80> from None via "None">

'''
This Score is the first Stream representing this piece in music21 so
 it has no derivation origin. However, let’s look at the first couple
 of measures of the piece using .measures:
'''
sExcerpt = s.measures(1, 4)
sExcerpt.id = 'excerpt'
sExcerpt.show()
''' 
This excerpt has a more interesting derivation:'''
# print(sExcerpt.derivation)
# <Derivation of <music21.stream.Score excerpt> from 
# <music21.stream.Score mozartK80> via "measures">
'''There are three things that are reported by the __repr__ of the 
Derivation object: the client (that is the element housing the Derivation
 object), the origin (that is the Stream that the client was derived from),
 and the method that derived the new Stream:
'''
# print(sExcerpt.derivation.client)
# <music21.stream.Score excerpt>
# print(sExcerpt.derivation.origin)
# <music21.stream.Score mozartK80>
# print(sExcerpt.derivation.method)
# measures

'''
Let’s create another Stream from the Excerpt, this time, via transposition:'''
sTransposed = sExcerpt.transpose('P4')
sTransposed.show()
sTransposed.id = 'transposed'
print(sTransposed.derivation.origin)




