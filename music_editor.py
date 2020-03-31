import random

note2value = {"Ab":-1, "A":0, "A#":1, "Bb":1, "B":2, "C":3, "C#":4, "Db":4, "D":5, "D#":6, "Eb":6, "E":7, "F":8, "F#":9, "Gb":9, "G":10, "G#":11,}
value2note = { 0:"A", 1:"A#", 2:"B", 3:"C", 4:"C#", 5:"D", 6:"D#", 7:"E", 8:"F", 9:"F#", 10:"G", 11:"G#"}

class Note:
    def __init__(self, note_name, octave):
        self.note_name = note_name.capitalize()
        self.note_value = note2value[self.note_name]
        self.octave = octave
        self.total_note_value = self.octave * 12 + self.note_value

    def getNoteName(self):
        return self.note_name

    def getOctave(self):
        return self.octave

    def getTotalValue(self):
        return self.total_note_value

    def distance(self, other):
        return abs(self.total_note_value - other.total_note_value)

    def __repr__(self):
        return self.getNoteName() + str(self.getOctave())

    def __eq__(self, other):
        return other != None and (self.note_name == other.note_name and self.octave == other.octave)

    def __lt__(self, other):
        return self.octave < other.octave or (self.octave == other.octave and self.note_name < other.note_name)

    def __le__(self, other):
        return self < other or self == other


class Chord:
    def __init__(self, notes):
        self.notes = notes

    def getNotes(self):
        return self.notes

    def getNote(self, voice):
        return self.notes[voice]
    
    def setNote(self, voice, note):
        self.notes[voice] = note

    def __repr__(self):
        return str(self.notes)







class Solver:
    def __init__(self, melody):
        # This assumes a 4 voice 1st species counterpoint and melody starts on tonic
        self.melody = melody

        # FIXME
        soprano = self.melody[0]
        alto = Note(value2note[(soprano.getTotalValue() - 5) % 12], (soprano.getTotalValue() - 5) // 12)
        tenor = Note(value2note[(alto.getTotalValue() - 3) % 12], (alto.getTotalValue() - 3) // 12)
        bass = Note(value2note[(tenor.getTotalValue() - 4) % 12], (tenor.getTotalValue() - 4) // 12)
        first_chord = Chord([soprano, alto, tenor, bass])
        self.chords = [first_chord] + [Chord([note] + [None]*3) for note in self.melody[1:]]

    def getMelody(self):
        return self.melody

    def getChords(self):
        return self.chords

    def solve(self):
        """Just plug next possible value and backtrack if not possible"""
        variables = self._getVariables(self.chords)

        def solver(chords, variables):
            if not variables:
                return True
            chord_pos, voice = variables[0]

            # Get some right values to get possible next values
            prev_note = chords[chord_pos-1].getNote(voice) # Doesn't need check for if it is first chord because I already stated earlier that the 
                                                           # first chord is already given
            high_note = self._getHighNote(chords[chord_pos], voice)
            low_note = self._getLowNote(chords[chord_pos], voice)


            for note in self._nextNotes(prev_note, high_note, low_note, voice):
                print(chord_pos, voice, note)
                chords[chord_pos].setNote(voice, note)
                if self._valid(chords, chord_pos, voice):
                    if solver(chords, variables[1:]):
                        return True

                    chords[chord_pos].setNote(voice, None)

                chords[chord_pos].setNote(voice, None)
            return False

        return solver(self.chords, variables)

    def _getHighNote(self, chord, voice):
        high_note = None
        i = 1
        while high_note == None:
            high_note = chord.getNote(voice-i)
            i += 1

        return high_note

    def _getLowNote(self, chord, voice):
        low_note = None
        i = 1
        while low_note == None and voice+i < len(chord.getNotes()):
            low_note = chord.getNote(voice+i)
            i += 1

        if low_note == None:
            voice_above = self._getHighNote(chord, voice)
            low_note = Note(voice_above.getNoteName(), voice_above.getOctave() - 1)

        return low_note

    def _nextNotes(self, prev_note, high_note, low_note, voice):
        """Generates next possible notes

        >>> solve = Solver([])
        >>> solve._nextNotes(Note("E", 4), Note("G#", 4), Note("Db", 4))
        [F4, D#4, F#4, D4, G4, C#4, G#4]
        """
        distance = 1
        high_bound = prev_note.distance(high_note)
        low_bound = prev_note.distance(low_note)
        bound = max([high_bound, low_bound])
        # notes = [prev_note]
        notes = []
        if voice in [1, 2]:
            notes.append(prev_note)
        while distance <= bound:
            if distance <= high_bound:
                total_note_value = prev_note.getTotalValue() + 1 * distance
                note = Note(value2note[total_note_value % 12], total_note_value//12)
                notes.append(note)

            if distance <= low_bound:
                total_note_value = prev_note.getTotalValue() - 1 * distance
                note = Note(value2note[total_note_value % 12], total_note_value//12)
                print(prev_note, note)
                notes.append(note)
            
            distance += 1

        return notes

    def _isConsecutive(self, chord1, chord2):
        """Checks to see if there are any consecutive 5ths or 8ths

        >>> solve = Solver([])
        >>> solve._isConsecutive(Chord([Note("E", 4), Note("A", 4)]), Chord([Note("D", 4), Note("G", 3)]))
        True
        >>> solve._isConsecutive(Chord([Note("E", 4), Note("B", 4)]), Chord([Note("D", 4), Note("G", 3)]))
        True
        >>> solve._isConsecutive(Chord([Note("E", 4), Note("C", 4)]), Chord([Note("D", 4), Note("G", 3)]))
        True
        >>> solve._isConsecutive(Chord([Note("C", 4), Note("F", 3)]), Chord([Note("D", 4), Note("G", 3)]))
        True
        >>> solve._isConsecutive(Chord([Note("A", 4), Note("F", 3)]), Chord([Note("D", 4), Note("G", 3)]))
        True
        >>> solve._isConsecutive(Chord([Note("E", 4), Note("F", 3)]), Chord([Note("D", 4), Note("G", 3)]))
        False
        """
        for voice1, note1 in enumerate(chord2.getNotes()):
            if note1 != None:
                for voice2, note2 in enumerate(chord2.getNotes()[voice1+1:]):
                    if note2 != None:
                        voice2 += voice1 + 1
                        if note1.distance(note2) in [6, 7, 12]:
                            if (chord1.getNote(voice1).distance(chord1.getNote(voice2)) % 12) in [0, 6, 7]:   # Check if parallel
                                return True
                            elif chord1.getNote(voice1) < note1 and chord1.getNote(voice2) < note2: # Check if consecutive upward
                                return True
                            elif chord1.getNote(voice1) > note1 and chord1.getNote(voice2) > note2: # Check if consecutive downward
                                return True

        return False

    def _isChord(self, chord):
        if chord.getNotes()[-1] == None:
            return True

        bass = chord.getNotes()[-1]
        for voice, note1 in enumerate(chord.getNotes()):
            if (note1.distance(bass) % 12) not in [0, 3, 4, 7, 8, 9]:
                return False

            for note2 in chord.getNotes()[voice:]:
                if note1.distance(note2) % 12 == 1:
                    return False
                if note1.distance(note2) == 0:
                    if not random.randint(0, 5):
                        return False

        return True

    def _valid(self, chords, chord_pos, voice):
        """Checks if the note is valid"""
        if (0 != chord_pos) and self._isConsecutive(chords[chord_pos-1], chords[chord_pos]): # Checks previous to current
            return False

        if (len(chords) > chord_pos + 1) and self._isConsecutive(chords[chord_pos], chords[chord_pos+1]): # Checks current to next
            return False

        if not self._isChord(chords[chord_pos]):
            return False

        return True

    def _getVariables(self, chords):
        return [(chord_pos, voice) for chord_pos in range(len(chords)) for voice in range(len(chords[chord_pos].getNotes())) if chords[chord_pos].getNote(voice) == None]




if __name__ == '__main__':
    melody = []
    for i in range(10):
        str_note = input()
        melody.append(Note(str_note[0], int(str_note[1])))

    solver = Solver(melody)
    solver.solve()
    print(solver.getChords())























