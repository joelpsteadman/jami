import Music
import midi #for reading and writing MIDI files
import re #regex for interpreting the midi.read_midifile() output
import MidiError

weightedRandom = []

#database that stores all the 4-note patterns
#in the form {[string of 8 digits] : [# of appearances]}
#where key is 4 2-digit numbers 0-11 representing the # of half-steps each note is above the tonic
fourNoteDatabase = {'total' : 0}
#database that stores all the 3-note patterns
#in the form {[string of 6 digits] : [# of appearances]}
#where key is 3 2-digit numbers 0-11 representing the # of half-steps each note is above the tonic
threeNoteDatabase = {'total' : 0}
#database that stores all the 2-note patterns
#in the form {[string of 4 digits] : [# of appearances]}
#where key is 2 2-digit numbers 0-11 representing the # of half-steps each note is above the tonic
twoNoteDatabase = {'total' : 0}
#database that stores all the 2-note harmonies
#in the form {[string of 4 digits] : [# of appearances]}
#where key is 2 2-digit numbers 0-11 representing the # of half-steps each note is above the tonic
harmonicDatabase = {'total' : 0}
#database that stores all the 1-note patterns
#in the form {[string of 2 digits] : [# of appearances]}
#where key is 1 2-digit numbers 0-11 representing the # of half-steps each note is above the tonic
oneNoteDatabase = {'total' : 0}

#reads all the MIDI files using the MIDI library
fileNames = './m/Air_on_the_G_String', './m/Bach_Capriccio_in_Bb_Major_VI._Fugue', './m/BWV_245', './m/Chorale', './m/Das_walt_mein_Gott_Vater_Sohn_und_heilger_Geist', './m/Freu_dich_sehr_o_meine_seele', './m/Ich_dank_dir_lieber_Herre', './m/Jesu_meine_Freude', './m/Matthaus_Passion_Choral_No_63__O_Haupt_voll_Blut_und_Wunden', './m/Nun_danket_alle_Gott', './m/Nun_ruhen_alle_W_lder', './m/Oh_Haupt_voll_Blut_und_Wunden', './m/Orchestral_Suite_No.3', './m/Puer_natus_in_Betlehem', './m/Schafe_konnen_sicher_weiden', './m/Sei Lob und Preis mit Ehren', './m/Wachet_auf', './m/ADAGIO', './m/De_vesper', './m/Freude_trinken_alle_Wesen', './m/Inno_al_Creatore_di_', './m/Minuet_in_G', './m/Ode_to_Joy', './m/Sonata No. 14 3rd Movement', './m/Turkish_March', './m/El_Capitan', './m/Semper_Fidelis', './m/The_Gladiator_March-1', './m/The_Gladiator_March-2', './m/The_Stars_and_Stripes_Forever-1', './m/The_Stars_and_Stripes_Forever-2', './m/LIEBE', './m/Pilgrims_Chorus', './m/Svatebni_pochod_z_opery_Lohengrin', './m/Wedding_March'
midiFiles = []
for name in fileNames:
	name += '.mid'
	midiFiles.append(str(midi.read_midifile(name)))

#reads all the harmony MIDI files using the MIDI library
patternH1 = str(midi.read_midifile("./m/H1.mid"))
patternH2 = str(midi.read_midifile("./m/H2.mid"))
patternH3 = str(midi.read_midifile("./m/H3.mid"))
patternH4 = str(midi.read_midifile("./m/H4.mid"))
patternH5 = str(midi.read_midifile("./m/H5.mid"))
patternH6 = str(midi.read_midifile("./m/H6.mid"))
patternH7 = str(midi.read_midifile("./m/H7.mid"))
patternH8 = str(midi.read_midifile("./m/H8.mid"))
patternH9 = str(midi.read_midifile("./m/H9.mid"))
patternH10 = str(midi.read_midifile("./m/H10.mid"))
patternH11 = str(midi.read_midifile("./m/H11.mid"))
patternH12 = str(midi.read_midifile("./m/H12.mid"))
patternH13 = str(midi.read_midifile("./m/H13.mid"))
patternH14 = str(midi.read_midifile("./m/H14.mid"))
#patternH15 = str(midi.read_midifile("H15.mid"))
patternH16 = str(midi.read_midifile("./m/H16.mid"))
patternH17 = str(midi.read_midifile("./m/H17.mid"))
patternH18 = str(midi.read_midifile("./m/h18.mid"))
patternH19 = str(midi.read_midifile("./m/h19.mid"))
patternH20 = str(midi.read_midifile("./m/H20.mid"))
patternH21 = str(midi.read_midifile("./m/H21.mid"))
patternH22 = str(midi.read_midifile("./m/H22.mid"))
patternH23 = str(midi.read_midifile("./m/H23.mid"))
patternH24 = str(midi.read_midifile("./m/H24.mid"))
patternH25 = str(midi.read_midifile("./m/H25.mid"))
patternH26 = str(midi.read_midifile("./m/H26.mid"))
patternH27 = str(midi.read_midifile("./m/H27.mid"))

#list of read out put from all harmony MIDI files
harmonyMidiFiles = [patternH1, patternH2, patternH3, patternH4, patternH5, patternH6, patternH7, patternH8, patternH9, patternH10, patternH11, patternH12, patternH13, patternH14,patternH16, patternH17, patternH18, patternH19, patternH20, patternH21, patternH22, patternH23, patternH24, patternH25, patternH26, patternH27]

def storeInDatabase(list, database):
	#list is a list of notes (numbers 0-11) or harmonies
	#database is one of the global databases 
	#assumes list has already been converted to semitone form
	#overloaded to work with all datbases in their own way
	#no return
	if database == threeNoteDatabase:
		if len(list) < 3:
			raise MidiError('Incomplete mume!')
		firstNote = 0
		while firstNote + 2 < len(list):
			mume = str(list[firstNote][0]) + str(list[firstNote + 1][0]) + str(list[firstNote + 2][0])
			addPattern(mume, threeNoteDatabase)
			firstNote += 1
			threeNoteDatabase['total'] += 1
	elif database == twoNoteDatabase:
		if len(list) < 2:
			raise MidiError('Incomplete mume!')
		firstNote = 0
		while firstNote + 1 < len(list):
			mume = str(list[firstNote][0]) + str(list[firstNote + 1][0])
			addPattern(mume, twoNoteDatabase)
			firstNote += 1
			twoNoteDatabase['total'] += 1
	elif database == oneNoteDatabase:
		if len(list) < 1:
			raise MidiError('Incomplete mume!')
		firstNote = 0
		while firstNote < len(list):
			mume = str(list[firstNote][0])
			addPattern(mume, oneNoteDatabase)
			oneNoteDatabase['total'] += 1
			firstNote += 1
	elif database == fourNoteDatabase:
		if len(list) < 4:
			raise MidiError('Incomplete mume!')
		firstNote = 0
		while firstNote + 3 < len(list):
			mume = str(list[firstNote][0]) + str(list[firstNote + 1][0]) + str(list[firstNote + 2][0]) + str(list[firstNote + 3][0])
			addPattern(mume, fourNoteDatabase)
			firstNote += 1
			fourNoteDatabase['total'] += 1
	elif database == harmonicDatabase:
		for harmony in list:
			harmony = str(harmony)
			addPattern(harmony, harmonicDatabase)
			harmonicDatabase['total'] += 1
	else:
		raise MidiError('Nonexistent database')

def addPattern(pattern, dictionary):
	#adds a specified pattern to the database specified
	#param 'pattern' is a musical pattern
	if(dictionary.has_key(pattern)): #pattern has already been added to dictionary
		dictionary[pattern] += 1
	else:
		dictionary[pattern] = 1

def setupWeightedRandom():
	for i in oneNoteDatabase:
		for j in range(0, oneNoteDatabase[i]):
			if j != 'total':
				weightedRandom.append(i)

def initializeFiles():
	#TODO shouldn't be more than one key signature event so I should check for that
	for i in range(len(midiFiles)): #for each quartet file
		keySignatureEvents = re.findall(r'midi.KeySignatureEvent\(tick=[0-9]+, data=\[[0-9]+, [0-9]+]\)',midiFiles[i], re.M)
		trackEvents = re.findall(r'midi\.Track.*[\s]*\[(midi(.*[\s]*))*(TrackE)',midiFiles[i], re.M)
		timeSignatureEvents = re.findall(r'midi\.TimeSignatureEvent\(tick=[0-9]+, data=\[[0-9]+, [0-9]+, [0-9]+, [0-9]+\]',midiFiles[i], re.M)
		a = -1
		b = -1
		for x in keySignatureEvents:
			keySigMatch = re.match( r'.*data=\[([0-9]+), [0-9]+]\)', x)
			if a != -1 and keySigMatch.group(1) != a:
				print "Warning: Conflicting key signatures given in file \'", fileNames[i], '(', i ,')',  "\'!"
			a = keySigMatch.group(1)
			if keySigMatch:
				Music.keySignature = Music.setKeySignature(keySigMatch.group(1))
		for x in timeSignatureEvents:
			timeSigMatch = re.match( r'midi\.TimeSignatureEvent\(tick=[0-9]+, data=\[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)\]', x)
			if a != -1 and b != -1 and timeSigMatch.group(1) != a and timeSigMatch.group(2) != b:
				print "Warning: Conflicting time signatures given in file \'", fileNames[i], '(', i ,')', "\'!"
			a = timeSigMatch.group(1)
			b = timeSigMatch.group(2)
			if timeSigMatch:
				Music.setTimeSignature(timeSigMatch.group(1), timeSigMatch.group(2))
		for t in trackEvents:
			noteOnEvents = re.findall(r'(midi.NoteOnEvent\(tick=[0-9]+, channel=[0-9]+, data=\[[0-9]+, [1-9][0-9]*]\))', midiFiles[i], re.M)
			notes = []
			for x in noteOnEvents:
				noteOnMatch = re.match( r'.*tick=([0-9]+), channel=[0-9]+, data=\[([0-9]+), [1-9][0-9]*]', x)
				if noteOnMatch:
					data = [Music.convertToSemiTone(noteOnMatch.group(2)), noteOnMatch.group(1), 0]
					notes.append(data)
			if len(notes) < 4:
				raise MidiError('Midi file too short to analyze mumes')
			storeInDatabase(notes, fourNoteDatabase)
			storeInDatabase(notes, threeNoteDatabase)
			storeInDatabase(notes, twoNoteDatabase)
			storeInDatabase(notes, oneNoteDatabase)
	setupWeightedRandom()

def storeHarmonies():
	#TODO recognize all harmony combinations when more than 2 notes start simultaniously
	for i in range(len(harmonyMidiFiles)):
		harmonyEvents = re.findall(r'[.]*midi.NoteOnEvent\(tick=[0-9]+, channel=[0-9]+, data=\[[0-9]+, [1-9][0-9]*]\)\,[\s]*midi.NoteOnEvent\(tick=0, channel=[0-9]+, data=\[[0-9]+, [1-9][0-9]*]\)', harmonyMidiFiles[i], re.M)
		harmonies = []
		if len(harmonyEvents) == 0:
			print 'H', i+1, 'has no harmonies?!?'
		for x in harmonyEvents:
			matchObj = re.match(r'midi.NoteOnEvent\(tick=[0-9]+, channel=[0-9]+, data=\[([0-9]+), [1-9][0-9]*]\)\,[\s]*midi.NoteOnEvent\(tick=0, channel=[0-9]+, data=\[([0-9]+), [1-9][0-9]*]\)', x)
			topNote = Music.convertToSemiTone(matchObj.group(1))
			bottomNote = Music.convertToSemiTone(matchObj.group(2))
			harmony1 = str(topNote) + str(bottomNote)
			harmonies.append(harmony1)
			if bottomNote != topNote:
				harmony2 = str(bottomNote) + str(topNote)
				harmonies.append(harmony2)
		storeInDatabase(harmonies, harmonicDatabase)

#Base code for quicksort taken from http://www.geeksforgeeks.org/iterative-quick-sort/
def partition(arr,low,high):
	i = ( low-1 ) # index of smaller element
	pivot = arr[high] # pivot
	for j in range(low , high):
		# If current element is smaller than or
		# equal to pivot
		if arr[j].less_than_or_equal(pivot):
			# increment index of smaller element
			i = i+1
			arr[i],arr[j] = arr[j],arr[i]
	arr[i+1],arr[high] = arr[high],arr[i+1]
	return ( i+1 )

# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index

# Function to do Quick sort
def quickSort(arr,low,high):
	if low < high:
		# pi is partitioning index, arr[p] is now
		# at right place
		pi = partition(arr,low,high)
		# Separately sort elements before
		# partition and after partition
		quickSort(arr, low, pi-1)
		quickSort(arr, pi+1, high)

def sort(list):
	quickSort(list, 0, len(list) - 1)