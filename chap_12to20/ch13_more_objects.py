import  music21 as m 

# At this point you know how to find a Music21Object, how to name them and group them (with .id and .groups)
#  and how to position them in Streams (with .offset, .priority, .classSortOrder and the .activeSite)

###########   .sites   ############
# All Music21Objects have a .sites property which is a Sites object which holds information 
# about all the places the Music21Object is stored in. 

n = m.note.Note()
s1 = m.stream.Stream(id='s1')
s2 = m.stream.Stream(id='s2')
s1.insert(10, n)
s2.insert(20, n)
for s in n.sites:
    print(s, s.elementOffset(n))