import music21 as m21 

# We can parse the score from the corpus with:
sBach = m21.corpus.parse('bach/bwv57.8')
print('sBach len: ', len(sBach))
# sBach.show()  # uncomment to show page on musescore

# print('Parts: ', len(sBach.getElementsByClass(m21.stream.Part))) or
print('Parts: ', len(sBach.parts))

print('Measure in sopranos part: ', len(sBach.getElementsByClass(m21.stream.Part)[0]\
    .getElementsByClass(m21.stream.Measure)))
print("Notes in measure 2 sopranos: ", len(sBach.getElementsByClass(m21.stream.Part)[0].\
    getElementsByClass(m21.stream.Measure)[1].getElementsByClass(m21.note.Note)))
print("Notes in measure 2 tenor: ", len(sBach.getElementsByClass(m21.stream.Part)[2].\
    getElementsByClass(m21.stream.Measure)[1].getElementsByClass(m21.note.Note)))