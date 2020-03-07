import music21 as m21

# The basic:
# If the number for a duration is omitted, then the next note uses the previous note’s duration:
s = m21.converter.parse('tinyNotation: 4/4 C4 D E F G A B c')
# s.show()

# Case determines octave: “C” = the c in bass clef (C3) while “c” = middle C (C4). 
s = m21.converter.parse("tinyNotation: 4/4 CC4 C4 c2")
# s.show()

# Periods signify dots, “r” is for a rest, and “~” indicates a tie:
s = m21.converter.parse('tinyNotation: 4/4 C4 D E8 F G16 A B c C.4 D8~ D8 r c4')
# s.show()

# Sharps, flats, and, if desired for clarity, naturals are indicated with #, - (not b) and, n, respectively:
s = m21.converter.parse('tinyNotation: 4/4 c4 c# c c## cn c- c-- c c1')
# s.show()

# A lyric syllable is specified by appending it after the note with an underscore:
s = m21.converter.parse('tinyNotation: 4/4 c4_Ale- d2_lu- e4_ia')
# s.show()

# triplets are possible by enclosing the triplet notes in curly brackets along with a special trip prefix:
s = m21.converter.parse('tinyNotation: 4/4 c4 trip{c8 d e} trip{f4 g a} b-1')
# s.show()

# Applying an id to a note with the “=” tag, and then make changes to it using music21:
s = m21.converter.parse('tinyNotation: 4/4 c4 d=id2 e f')
n = s.recurse().getElementById('id2')
ch = m21.chord.Chord('D4 F#4 A4')
ch.style.color = 'blue'
n.activeSite.replace(n, ch)
# s.show()

# And that’s how we use TinyNotation, about 90% of the time. 
# But when I need to, I can make something more complex we can expanding 
# TinyNotation through new tokens (like the Notes, Rests, and TimeSignatures), 
# modifiers (such as the = for assigning .id, or the _ for assigning a lyric) and 
# states (such as the triplet state enclosed in curly brackets).

# The first thing that we’ll need to know in order to expand TinyNotation is how to get 
# at the TinyNotation Converter itself (which is different from the basic converter.parse() call). 
# It’s found in the tinyNotation module, and is called with a set of music to parse.
tnc = m21.tinyNotation.Converter('6/8 e4. d8 c# d e2.')
# We run the converter by calling .parse() on it and then there will be a 
# Stream (generally a stream.Part object) in the .stream attribute of the Converter.
tnc.parse()
s = tnc.stream
# s.show()

######################    Beyond the tiny notation    ###################

######################    Adding new tokens           ###################

# TinyNotation does not have a way of specifying the Key (and thereby the KeySignature) of a piece or region.
#  Let’s add that “one more thing” with a new Token:
class KeyToken(m21.tinyNotation.Token):
    def parse(self, parent):
        keyName = self.token
        return m21.key.Key(keyName)
# The KeyToken is a subclass of the tinyNotation.Token class. When it is parsed, .parse() is 
# called and it is passed a reference to the Converter object, and important information is stored 
# in the self.token attribute. The Converter calling parse() expects that a Music21Object or None will
# be returned.Here we’re going to return a Key object.
# Now that we’ve defined this particular Token, we’ll need to teach the Converter when to call it.
# We’ll say that any token (that is, data separated by spaces) which begins with a k is a new Key object,
# and that the relevant data is everything after the k. And we’ll add this to a blank Converter object.
tnc = m21.tinyNotation.Converter()
keyMapping = (r'k(.*)', KeyToken)
tnc.tokenMap.append(keyMapping)
# Next, let’s create a fragment of TinyNotation to see if this works, using the load() method:
tnc.load('4/4 kE- G4 A G B kf# A1')
tnc.parse()
s = tnc.stream
# s.show()

######################    Modify existing tokens           ###################


# Now that we have a way to create totally new Tokens, let’s look at ways we can modify existing tokens. 
# Let’s first create a simple Modifier that changes the color of individual notes after they’ve been parsed:
class ColorModifier(m21.tinyNotation.Modifier):
    def postParse(self, m21Obj):
        m21Obj.style.color = self.modifierData
        return m21Obj
# Now we’ll modify our Converter object to make it so that the ColorModifier is run anytime that a color
#  name is put in angle brackets after a Token, and then test it on a simple stream.
tnc.modifierAngle = ColorModifier
tnc.load('3/4 c4<red> d<green> e-<blue>')
tnc.parse()
# tnc.stream.show()

# Here’s a less silly modifier which replaces the Note object that comes in with a ChordSymbol object 
# that combines the root name from the Note with the data from the modifier:
class HarmonyModifier(m21.tinyNotation.Modifier):
    def postParse(self, n):
        cs = m21.harmony.ChordSymbol(n.pitch.name + self.modifierData)
        cs.duration = n.duration
        return cs

tnc.modifierUnderscore = HarmonyModifier
tnc.load('4/4 C2_maj7 D4_m E-_sus4')
# tnc.parse().stream.show('t')

# If we leave in the bass note and instead add the ChordSymbol to the stream, 
# then we’ll be able to see it on the score:
class HarmonyModifier(m21.tinyNotation.Modifier):
    def postParse(self, n):
        cs = m21.harmony.ChordSymbol(n.pitch.name + self.modifierData)
        self.parent().stream.append(cs)
        return n

tnc.modifierUnderscore = HarmonyModifier
tnc.load('4/4 C2_maj7 D4_m E-_sus4')
# tnc.parse().stream.show()
# tnc.parse().stream.show('t')

######################    Defining a Satate for a set of tokens    ###################

# Lastly are State conditions. These affect more than one Token at a time and are (generally)
#  enclosed in curly brackets (the “TieState” is a State that works differently but is too 
# advanced to discuss here). 
# Let’s create a silly State first, that removes stems from notes when it’s closed:

class NoStemState(m21.tinyNotation.State):
    def end(self):
        for n in self.affectedTokens:
            n.stemDirection = 'none'
    
# Every State token has the following methods called: 
# start(), which is called when the state is begun, 
# affectTokenBeforeParse(tokenStr) which gives the State object the opportunity to change the 
#       string representation of the token before it is parsed, 
# affectTokenAfterParseBeforeModifier(music21object) which lets the music21 object be changed
#       before the modifiers are applied, 
# affectTokenAfterParse(music21object) which lets the state change the music21 object after
#       all modifiers are applied, and 
# end() which lets any object in the .affectedToken list be changed after it has been appended 
#       to the Stream. Often end() is all you will need to set.

# Now we’ll define "nostem" to be the start of a stemless state. We do this by adding 
# the term “nostem” to the bracketStateMapping dictionary on TinyNotationConverter.


tnc.bracketStateMapping['nostem'] = NoStemState
# tnc.load("4/4 c4 d e f g2 a4 b c'1")
tnc.load("4/4 c4 d nostem{e f g2 a4} b c'1")
# tnc.parse().stream.show()

# Using State to create chords. 
# To do this, we will prevent notes from being added to the stream as they are parsed, 
# and then put a Chord into the stream at the end:

class ChordState(m21.tinyNotation.State):
    def affectTokenAfterParse(self, n):
       super(ChordState, self).affectTokenAfterParse(n)
       return None # do not append Note object

    def end(self):
        ch = m21.chord.Chord(self.affectedTokens)
        ch.duration = self.affectedTokens[0].duration
        return ch

tnc.bracketStateMapping['chord'] = ChordState
tnc.load("2/4 C4 chord{C4 e g} F.4 chord{D8 F# A}")
tnc.parse().stream.show()