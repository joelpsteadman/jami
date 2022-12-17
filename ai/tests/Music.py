import random
import Database
import MidiError

solfege = ['Do','Ra','Re','Me','Mi','Fa','Fi','So','Si','La','Te','Ti']
diatonicPitches = ['00', '02', '04', '05', '07', '09', '11']
allPitches = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']

#used to interpret MIDI representations of notes which are 0-127 for C0 - G10
keys = {
'C' : 0,
'CSHARP' : -1,
'DFLAT' : -1,
'D' : -2,
'EFLAT' : -3,
'E' : -4,
'F' : -5,
'FSHARP' : -6,
'GFLAT' : -6,
'G' : -7,
'AFLAT' : -8,
'A' : -9,
'BFLAT' : -10,
'B' : -11,
'CFLAT' : -11
}
keySignature = 'C'
timeSignature = 0.0

def setKeySignature(num):
	#interprets the given key signature code to avoid magic numbers
	#param 'num' is key signature code from midi.read
	#0-7 represent # of sharps in key signature
	#255-249 represent (256-num) flats in the key signature
	#assumes a major key
	#returns the key as refered to in music as a string
	if num == '0':
		return 'C'
	elif num == '1':
		return 'G'
	elif num == '2':
		return 'D'
	elif num == '3':
		return 'A'
	elif num == '4':
		return 'E'
	elif num == '5':
		return 'B'
	elif num == '6':
		return 'FSHARP'
	elif num == '7':
		return 'CSHARP'
	elif num == '255':
		return 'F'
	elif num == '254':
		return 'BFLAT'
	elif num == '253':
		return 'EFLAT'
	elif num == '252':
		return 'AFLAT'
	elif num == '251':
		return 'DFLAT'
	elif num == '250':
		return 'GFLAT'
	elif num == '249':
		return 'CFLAT'
	else:
		print('Error: unrecognized key signature code')

def setTimeSignature(num, denom):
	timeSignature = float(num) / (2 ** float(denom))

def convertToSemiTone(note):
	#'note' should be an int (0-127)
	#requires that key signature has already been set and that it is a major key
	#returns a note 0-12; 0 corresponds to Do, 1 to Di/Ra, etc.
	#assumes direction of notes (up or down) does not matter
	note = (int(note) + int(keys[keySignature])) % 12 #
	if note < 10:
		note = '0' + str(note)
	return note

def harmonize(notes, type):
	#bootstraps / overrides? harmonize methods
	if type == 'random':
		return randomHarmonize()
	elif type == 'diatonic':
		return diatonicHarmonize()
	elif type == 'smart' and len(notes) < 2:
		return smartHarmonize1(notes[0])
	elif type == 'smart':
		return smartHarmonizeGroup(notes)
	else:
		raise MidiError('Boo!')
		
def smartHarmonize1(note):
	#note is a midi note string of 2 digits 00-11
	#returns a smart harmony for this note
	options = []
	diatonicPitches = ['00', '02', '04', '05', '07', '09', '11']
	for harmony in diatonicPitches:
		key = harmony + note
		if Database.harmonicDatabase.has_key(key):
			n = 0
			while n < Database.harmonicDatabase[key]:
				options.append(key)
				n += 1
	choice = random.randint(0, len(options) - 1)
	pick = options[choice]
	return pick[:2]

def smartHarmonizeGroup(notes):
	#note is a midi note string of 2 digits 00-11
	#returns a harmony for this note
	options = []
	diatonicPitches = ['00', '02', '04', '05', '07', '09', '11']
	for note in notes:
		for harmony in diatonicPitches:
			key = harmony + note
			if Database.harmonicDatabase.has_key(key):
				n = 0
				number = Database.harmonicDatabase[key]
				for i in notes:
					if i == int(key[:2]):#if this is the same as the other notes on this beat, make it less likely
						number /= 2
				while n < number:
					options.append(key)
					n += 1
	choice = random.randint(0, len(options) - 1)
	pick = options[choice]
	return pick[:2]

def diatonicHarmonize():
	#note is a midi note string of 2 digits 00-11
	#returns a diatonic harmony for this note
	note = diatonicPitches[random.randint(0,6)]
	return note

def randomHarmonize():
	#note is a midi note string of 2 digits 00-11
	#returns a random harmony for this note
	pick = allPitches[random.randint(0,11)] #Database.weightedRandom[random.randint(0, len(Database.weightedRandom) - 1)]
	return pick