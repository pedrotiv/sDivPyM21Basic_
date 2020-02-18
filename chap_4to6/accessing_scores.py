import music21 as m21 

# We can parse the score from the corpus with:
sBach = m21.corpus.parse('bach/bwv57.8')
print("sBach score's len: ", len(sBach))
# sBach.show()  # uncomment to show page on musescore

# There are three forms to get the number of the parts, ie:
# print('Parts: ', len(sBach.getElementsByClass(m21.stream.Part))) or
# len(sBach.getElementsByClass('Part')) or more usully:
print('Parts in the score: ', len(sBach.parts))

print("Measure in soprano's part: ", len(sBach.getElementsByClass(m21.stream.Part)[0]\
    .getElementsByClass(m21.stream.Measure)))
print("Notes in second measure of soprano part: ", len(sBach.getElementsByClass(m21.stream.Part)[0].\
    getElementsByClass(m21.stream.Measure)[1].getElementsByClass(m21.note.Note)))
print("Notes in second measure of tenor part: ", len(sBach.getElementsByClass(m21.stream.Part)[2].\
    getElementsByClass(m21.stream.Measure)[1].getElementsByClass(m21.note.Note)))

alto = sBach.parts[1] # parts count from zero, so soprano is 0 and alto is 1
excerpt = alto.measures(1, 4)
print('Compass 1 to 4, alto:')
excerpt.show('text')
print('\nOnly compass number 2, alto')
measure2 = alto.measure(2) # measure not measure_s_
measure2.show('text')

# What is great about .measure() and .measures() is that they can work on a whole score and not just a single part
measureStack = sBach.measures(2, 3)
measureStack.show()