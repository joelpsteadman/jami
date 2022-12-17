import time #to time algorithms
t0 = time.time()# times start-up time
import random #for random note generation
print('Scanning MIDI files - this may take a moment..')
import Database
import Music
import sys, os #for pretty printing and memory measurement
import MidiError

'''
**THE FOLLOWING ARE IDEAS I WANTED TO IMPLEMENT BUT HAVE NOT YET HAD THE TIME FOR**
#TODO put database into a csv*? file and load upon start-up
#TODO annalyze harmonies from quartet music rather than H files
#TODO get MIDI files from a folder
#TODO add rhythm
#TODO make harmonic database combinations rather than orientation specific
#TODO fix bug with combinations of random, diatonic, and smart
#TODO create python warnings instead of printing them in Database module
#TODO store notes as bytes or ints instead of strings to save space
#TODO factor in two and four note permutations to develope better score
#TODO find a way to make it learn that variation is preferable to repeating the same note over and over
#TODO make work with tunes of odd # melody-length
#TODO make a anti-smart attempt / harmonize that intentionally makes 'bad' tunes
#TODO check that all key signatures are read correctly
#TODO fix 'Score your own melody'
#TODO add incentive based on batabase to have variety
#TODO chord progressions?

#TODO another AI that knows all formal music theory rules and finds which ones are most important based on feedback
'''

tuneAttempts = [] #list of all Tunes created by program

class Tune:
	def __init__(self, melody, harmony, type):
		#melody is a list of notes as strings in the form ['00', '02', etc.]
		#harmony is a list of lists of notes as strings in the form [['00', '02', etc.], ['00', '02', etc.], etc]
		#type describes with what method the Tune was created in the form of a string 'random' | 'diatonic' | 'smart'
		self.melody = melody
		self.harmony = harmony
		self.type = type
		self.score = 0
	def display(self):
		#for pretty printing a tunes data
		for note_index in self.melody:
			sys.stdout.write(Music.solfege[int(note_index)]+'  ')
		print
		for list_index in range(len(self.harmony)):
			sys.stdout.write(Music.solfege[int(self.harmony[list_index][0])]+'  ')
			for note_index in range(1, len(self.harmony[list_index])-1):
				sys.stdout.write(Music.solfege[int(self.harmony[list_index][note_index])]+'      ')
			sys.stdout.write(Music.solfege[int(self.harmony[list_index][len(self.harmony[list_index])-1])])
			print
		sys.stdout.write('TYPE: '+self.type)
		print('\tSCORE:', self.score)
	def less_than_or_equal(self, other):
		#used in quicksort algorithm in Database module
		if self.score <= other.score:
			return True
		else:
			return False
	def scoreMe(self, explain = False):
		#function 'score()' takes a Tune abject as its parameter, so a Tune must be created then scored
		self.score = score(self, explain)

def blockPrint():
	#Disable only used for now to avoid printing warnings when reading MIDI files
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
	#Restore temporary
    sys.stdout = sys.__stdout__

def attempt(length, type):
	#creates a tune from notes 0-12
	#param 'length' is the number of notes to be added to the tune
	#param 'type' indicates the method which will be used to create this tune
	
	#create melody
	melody = ['00']#first / last notes of melody will be the tonic
	if type == 'random':
		#creates a tune from randomly picking notes 0-12
		for i in range(1, int(length) - 1):
			#index = random.randint(0, len(Database.weightedRandom) - 1)
			note = Music.allPitches[random.randint(0,11)] #note = Database.weightedRandom[index]
			melody.append(str(note))
	elif type == 'diatonic':
		#creates a tune from randomly picking diatonic notes (notes in a major scale)
		for i in range(1, int(length) - 1):
			note = Music.diatonicPitches[random.randint(0,6)]
			melody.append(note)
	else:
		#creates a tune assigning more likely patterns more often than less likely patterns
		#TODO use two and four note patterns
		options = []
		#adds first 3 notes
		for i in range(12):
			for j in range(12):
				second = str(i)
				third = str(j)
				if i < 10:
					second = '0' + second
				if j < 10:
					third = '0' + third
				key = melody[0] + second + third
				if Database.threeNoteDatabase.has_key(key):
					n = 0
					while n < Database.threeNoteDatabase[key]:
						options.append(key)
						n += 1
		choice = random.randint(0, len(options) - 1)
		mume = options[choice]
		melody.append(mume[2:4])
		melody.append(mume[4:])
		#adds middle notes
		for i in range(3, int(length)-2):
			for j in range(12):
				third = str(j)
				if j < 10:
					third = '0' + third
				key = melody[i-2] + melody[i-1] + third
				if Database.threeNoteDatabase.has_key(key):
					n = 0
					while n < Database.threeNoteDatabase[key]:
						options.append(key)
						n += 1
			choice = random.randint(0, len(options) - 1)
			mume = options[choice]
			melody.append(mume[4:])
		#adds last two notes
		options = []
		for i in range(12):
			second = str(i)
			if i < 10:
				second = '0' + second
			key = melody[len(melody) - 3] + second + '00'
			if Database.threeNoteDatabase.has_key(key):
				for n in range(Database.threeNoteDatabase[key]):
					options.append(key)
		choice = random.randint(0, len(options) - 1)
		mume = options[choice]
		melody.append(mume[2:4])
	melody.append('00')
	
	#create harmonies
	notesToHarmonize = [melody[0]]
	for i in range(1, int(length)-1):#just interior notes in the melody
		if (i % 2) == 1:#adds every other note
			notesToHarmonize.append(melody[i])
	notesToHarmonize.append(melody[-1])
	listOfHarmoniesInThisAttempt = [notesToHarmonize]
	#add base harmony
	baseHarmony = ['00']
	for j in range(1, len(notesToHarmonize)-1):#just harmonize inner notes
		group = []
		for k in listOfHarmoniesInThisAttempt:
			group.append(k[j])
		baseHarmony.append(Music.harmonize(group, type))
	baseHarmony.append('00')#base harmony starts and ends with tonic
	for i in range(2):#add inner two harmonies
		harmony = []
		for j in range(len(notesToHarmonize)):
			group = []
			for k in listOfHarmoniesInThisAttempt:
				group.append(k[j])
			harmony.append(Music.harmonize(group, type))
		listOfHarmoniesInThisAttempt.append(harmony)
	listOfHarmoniesInThisAttempt.append(baseHarmony)
	listOfHarmoniesInThisAttempt.pop(0)#remove harmonies from the melody
	tune = Tune(melody, listOfHarmoniesInThisAttempt, type)
	tune.scoreMe()
	tuneAttempts.append(tune)

def score(tune, explain):
	#takes as input a Tune
	#param 'explain' is a boolean - if true, prints explanation of score
	#returns a score as a float for the given Tune representing the average standartd deviation
	'''
		      /__           \           /__           \ 
		     | >_ (# - avg.) |  +      | >_ (# - avg.) |
		     | _____________ |         | _____________ |
		.8 * |               |    .2 * |               |
		     |  stddev * (m) |         |  stddev * (h) |
		      \             /           \             / 
		
		m = # of mumes in the melody
		h = # of harmonies
	'''
	melstddev = 196.609503 #calculated previously in a spreadsheet
	harmstddev = 99.31675709 #"  "
	notestddev = 7488.941126 #"  "
	
	notescore = 0
	noteaverage = Database.oneNoteDatabase['total'] / 12.0 #12 is number of possible distinct
	numnotes = 0
	for i in range(len(tune.melody) - 2):
		#print(tune.melody[i]
		#print('# - avg = '
		#print((Database.oneNoteDatabase[tune.melody[i]]), noteaverage, (Database.oneNoteDatabase[tune.melody[i]]) - noteaverage
		notescore += (Database.oneNoteDatabase[tune.melody[i]]) - noteaverage
		numnotes += 1
	for i in range(len(tune.harmony)):
		for j in range(len(tune.harmony[i])):
			#print(tune.melody[i]
			#print('# - avg = '
			#print((Database.oneNoteDatabase[tune.harmony[i][j]]), noteaverage, (Database.oneNoteDatabase[tune.harmony[i][j]]) - noteaverage
			notescore += (Database.oneNoteDatabase[tune.harmony[i][j]]) - noteaverage
			numnotes += 1
	'''for n in tune.melody: #kind of stiff-arming - would be better to find another way to avoid chromaticism
		if n not in Music.diatonicPitches:
			melscore -= melaverage'''
	#print('total / (stddev * num)'
	#print(notescore, notestddev, numnotes
	#print(notescore / (notestddev * (numnotes))
	notescore = notescore / (notestddev * (numnotes))
	
	melscore = 0
	melaverage = Database.threeNoteDatabase['total'] / 1728.0 #1728 is number of possible distinct
	for i in range(0, len(tune.melody) - 2):
		mume = tune.melody[i] + tune.melody[i+1] + tune.melody[i+2]
		if Database.threeNoteDatabase.has_key(mume):
			melscore += (Database.threeNoteDatabase[mume]) - melaverage
		else:
			#pattern occures 0 times so reduce its score
			melscore += 0 - melaverage
	'''for n in tune.melody: #kind of stiff-arming - would be better to find another way to avoid chromaticism
		if n not in Music.diatonicPitches:
			melscore -= melaverage'''
	melscore = melscore / (melstddev * len(tune.melody))

	harmscore = 0
	harmnum = 0
	harmaverage = Database.harmonicDatabase['total'] / 144.0  #144 is number of possible distinct
	firstharm = ['00']
	for i in range(1, len(tune.melody)-1):
		if i % 2 == 1:
			firstharm.append(tune.melody[i])
	firstharm.append('00')
	allharms = [firstharm]
	for h in tune.harmony:
		allharms.append(h)
	mume = ''
	harms = len(allharms[0])
	for first in range(len(allharms)-1): #for first 3 harmony lines
		for second in range(first + 1, len(allharms)): # for every harmony line after first
			for j in range(harms): #for all harmonized positions in music
				mume = str(allharms[first][j]) + str(allharms[second][j])
				harmnum += 1
				if Database.harmonicDatabase.has_key(mume):
					harmscore += (Database.harmonicDatabase[mume]) - harmaverage
				else:
					#pattern occures 0 times so reduce its score
					harmscore += 0 - harmaverage
	'''for h in tune.harmony: #same stiff-arming as above
		for n in h:
			if n not in Music.diatonicPitches:
				harmscore -= harmaverage'''
	harmscore = harmscore / (harmstddev * harmnum)

	if explain:
		print('notescore:', notescore)
		print('melscore:', melscore)
		print('harmscore:', harmscore)
		print('melstddev:', melstddev)
		print('harmstddev:', harmstddev)
		print('melaverage:', melaverage)
		print('harmaverage:', harmaverage)
		print('score:', (.1 * melscore) + (.9 * harmscore))
	return (.1 * melscore) + (.5 * harmscore) + (.4 * notescore)

def displayBest(length, num):
	#TODO crashes when less than 10 attempts created
	num = int(num)
	print('len(tuneAttempts):', len(tuneAttempts))
	tuneList = []
	for i in range(10):
		tuneList.append(tuneAttempts[-(i+1)])
	for i in range(10):
		n = '#' + str(i+1)
		print('**********', n , '**********')
		tuneList[i].display()
		score(tuneList[i], True)
	print('************************')

def displaySample(length, num):
	num = int(num)
	print('len(tuneAttempts):', len(tuneAttempts))
	tuneList = []
	for i in range(11):
		tuneList.append(tuneAttempts[((len(tuneAttempts)-1) * i) / 10])
	i = 10
	while i >= 0:
		p = (i) * 10
		string = str(p) + '%'
		n = '#' + str(i+1)
		print('**********', string , '**********')
		tuneList[i].display()
		score(tuneList[i], True)
		print('******************************')
		i -= 1

def displayWorst(length, num):
	#TODO crashes when less than 10 attempts created
	num = int(num)
	print('len(tuneAttempts):', len(tuneAttempts))
	tuneList = []
	for i in range(10):
		tuneList.append(tuneAttempts[(i)])
	for i in range(10):
		n = '#' + str(i+1)
		print('**********', n , '**********')
		tuneList[i].display()
		score(tuneList[i], True)
	print('************************')

def createMIDIs():
	print('not implemented yet')

menu = '1) Create tunes\n' + '2) Results\n' + '3) Score your own melody\n' + '4) Give feedback\n' + '5) Create MIDIs\n' + '6) Exit\n'
resultsMenu = '1) Display best 10\n' + '2) Display Sample of Results\n' + '3) Display Worst 10\n'

blockPrint()
Database.initializeFiles()
Database.storeHarmonies()
enablePrint()

num = ''
type = ''
length = ''
done = False
t1 = time.time()
total = t1-t0
print('Database initialized in', total, 'seconds')
print('Three note permutations scanned:\t', Database.threeNoteDatabase['total'])
print('Two note permutations scanned:\t\t', Database.twoNoteDatabase['total'])
print('Four note permutations scanned:\t\t', Database.fourNoteDatabase['total'])
print('Harmonic combinations scanned:\t\t', Database.harmonicDatabase['total'])
while not done:
	choice = input(menu)
	if choice == '1':
		num = input('How many attempts would you like to make?\n')
		type = input('1) Random\n' + '2) Diatonic\n' + '3) Psuedoengineered\n')
		length = input('How long would you like your tune to be? (# of notes)\n')#TODO should put a lower and upper limit on this
		try:
			num = int(num)
		#TODO 
		except ValueError:
			print('Invalid number entered')
			break
		if type == '1'or type == '2'or type == '3':
			if type == '1':
				type = 'random'
			elif type == '2':
				type = 'diatonic'
			else:
				type = 'smart'
			num = float(num)
			counter = 0
			while counter < num:
				percent = -1
				if counter % 10000 == 0 or counter == num-1:
					string = ''
					print(str(int(round(counter * 100 / num, 0)))+'%')
					percent = round(counter * 100 / num, 0)
				attempt(length, type)
				counter += 1
		else:
			print('Sorry, ', type,' is an invalid option')
		t0 = time.time()
		Database.sort(tuneAttempts)
		t1 = time.time()
		total = t1-t0
		print(len(tuneAttempts), 'melodies sorted in', total, 'seconds!')
	elif choice == '2':
		resultsChoice = input(resultsMenu)
		if resultsChoice == '1':
			print(length)
			displayBest(length, num)
		elif resultsChoice == '2':
			displaySample(length, num)
		elif resultsChoice == '3':
			displayWorst(length, num)
	elif choice == '3':
		input = -2
		melody = []
		while input != -1:
			input = input('Enter note value (0-11) or \'done\' to complete melody\n')
			if input == 'done':
				print('Thank you for entering your melody!')
				input = -1
			else:
				if len(str(input)) < 2:
					input = '0' + input
				melody.append(str(input))
				if len(melody) > 2:
					print('That mume\'s (', melody[-3:],') score was: ', score(melody[-3:]))
					print('Melody current score:', score(melody))
		print('This melody\'s score is: ', score(melody))
	elif choice == '4':
		#TODO check that tuneAttempts is not empty
		feedback = input('Which melody did you like? (from among the top ten)\n')
		#TODO check for valid input
		tune = tuneAttempts[int(feedback) - 1]
		notes = tune.melody
		Database.storeInDatabase(notes, Database.fourNoteDatabase)
		Database.storeInDatabase(notes, Database.threeNoteDatabase)
		Database.storeInDatabase(notes, Database.twoNoteDatabase)
		Database.storeInDatabase(notes, Database.oneNoteDatabase)
		harmonizedMelodyNotes = [tune.melody[0]]
		for i in range(1, int(length)-1):#just interior notes in the melody
			if (i % 2) == 1:#adds every other note
				harmonizedMelodyNotes.append(tune.melody[i])
		harmonizedMelodyNotes.append(tune.melody[-1])
		listOfHarmonizedNotesInThisTune = [harmonizedMelodyNotes]#2d list
		for h in tune.harmony:
			listOfHarmonizedNotesInThisTune.append(h)
		harmonies = []
		for i in range(len(listOfHarmonizedNotesInThisTune)):
			for first in range(len(listOfHarmonizedNotesInThisTune) - 1):
				for second in range(first + 1, len(listOfHarmonizedNotesInThisTune)):
					harmonies.append(listOfHarmonizedNotesInThisTune[first][i] + listOfHarmonizedNotesInThisTune[second][i])
		Database.storeInDatabase(harmonies, Database.harmonicDatabase)
	elif choice == '5':
		createMIDIs()
		print('not implemented yet :(')
	elif choice == '6':
		done = True
		print('Goodbye!')
	else:
		print('Error: didn\'t enter a valid choice')