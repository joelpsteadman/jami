import sys
import binascii
import re
import error
<<<<<<< HEAD
import Note
import warnings
from music_classes import Song

=======
import warnings
from music_classes import Song

#TODO put functions in another file all together

>>>>>>> develop
#global variables
n1 = ""
n2 = ""
b2 = ""
b3 = ""
channel = 0
fp = 0
remaining_track_len = 0
new_event_type = True
num_events = 0
<<<<<<< HEAD

#TODO note position and duration need to be rounded and even then they are not rounded to an accurate value
def get_info(file_name):
=======
#Music Tools

#TODO note position and duration need to be rounded and even then they are not rounded to an accurate value
def get_info(file_name, verbose):

	def print_if_verbose(*strings):
		if verbose:
			s = ""
			for string in strings:
				s += str(string)
			print s

>>>>>>> develop
	channels = {}
	def set_channel(channel):
		channels[channel] = 1
	song = Song()
	global fp,remaining_track_len, channel, n1, n2, b2, b3
	f = open(file_name, "rb")
	data = "" #string containing the data of the file in hex
	try:
		byte = f.read(1)
		while byte != "":
			data += byte
			byte = f.read(1)
	finally:
		f.close()

	data = binascii.hexlify(data) #translate binary to hex
	n1 = ""
	n2 = ""
	b2 = ""
	b3 = ""
	channel = 0
	notes = {} #a dictionary of 16 lists of Notes cooresponding to their channel number
	for i in range(0,16):
		key = i
		notes[key] = list()
		'''
		notes now has the form:
		notes{
			0: ()
			1: ()
			2: ()
			3: ()
			4: ()
			5: ()
			6: ()
			7: ()
			8: ()
			9: ()
			10: ()
			11: ()
			12: ()
			13: ()
			14: ()
			15: ()
		}
		'''

	fp = 0 #file_position
	remaining_track_len = 0 #to check that the track length specified is correct

	def advance(nibbles): 
		'''updates fp and remaining_track_len
		'nibbles' is an integer representing the # of hex digits to advance
		Procedure (no return value)'''
		global fp, remaining_track_len
		fp += nibbles
		remaining_track_len -= nibbles

<<<<<<< HEAD
	def print_bytes(data, explanation = "", value = "", offset = 0):
=======
	def print_bytes(data, explanation = " ", value = " ", offset = 0):
>>>>>>> develop
		'''pretty-prints a small chunk of byte(s) and an explanation of what they mean in the MIDI file
		'data' is a string of hex values representing the bytes to be explained
		'explanation' is an optional string describing what the data means
		'value' is an optional string for a variable value related to the meaning of the data
		'offset' is a switch:
			odd values mean the data starts halfway through a byte
			even values means the data starts at the beginning of a byte
			there is no need to set this value to anything besides 0 or 1
		Procedure (no return value)
		'''
		i = offset
		string = ""
		for c in data:
			string += c
			if i % 2 == 1:
				string += " "
			i += 1
<<<<<<< HEAD
		#print string, "= ", explanation, value
=======
		print_if_verbose( string, "= ", explanation, value )
>>>>>>> develop

	#read header chunk:

	#check header chunk type
	if re.match(r'4d546864', data) == None:
		raise error.MidiException("File does not begin with \"MThd\"")
	fp = 8
	#check header length
	if re.match(r'00000006', data[fp:fp+8]) == None:
<<<<<<< HEAD
		raise error.MidiException("Unrecognized header length: expected \"00000006\", but got:", data[fp:fp+8])
=======
		raise error.MidiException("Unrecognized header length: expected \"00000006\", but got: ", data[fp:fp+8])
>>>>>>> develop
	fp += 8
	#check format
	midi_format = int(data[fp:fp+4], 16)
	if midi_format > 2:
<<<<<<< HEAD
		raise error.MidiException("Unrecognized format: expected 0,1, or 2, but got:", int(data[fp:fp+4], 16))
=======
		raise error.MidiException("Unrecognized format: expected 0,1, or 2, but got: ", int(data[fp:fp+4], 16))
>>>>>>> develop
	fp += 4
	#get number of tracks
	num_tracks = int(data[fp:fp+4], 16)
	fp += 4
<<<<<<< HEAD
	print_bytes(data[fp:fp+4], "Number of tracks:", num_tracks)
	song.num_tracks = num_tracks
	#get division data 
	division = data[fp:fp+4]
	print_bytes(data[fp:fp+4], "Division:", division)
	frmt = division[0:1]
	print_bytes(division[0:1], "Format:", frmt)
	ticks_per_quarter_note = int(division[1:], 16)
	if int(frmt, 16) < 8:
		print_bytes(division[1:], "Ticks per quarter note:", ticks_per_quarter_note, 1)
	#else:
		#print "Negative two's compliment of", int(division[1:2], 16) - 128, "frames / second"
		#print int(data[fp:fp+2],16), "ticks / frame"
	fp += 4
		
	#print "READ HEADER CHUNK OF SIZE", fp, "RESTARTING fp at position", fp
=======
	print_bytes(data[fp:fp+4], "Number of tracks: ", num_tracks)
	song.set_num_tracks(num_tracks)
	#get division data 
	division = data[fp:fp+4]
	print_bytes(data[fp:fp+4], "Division: ", division)
	frmt = division[0:1]
	print_bytes(division[0:1], "Format: ", frmt)
	ticks_per_quarter_note = int(division[1:], 16)
	if int(frmt, 16) < 8:
		print_bytes(division[1:], "Ticks per quarter note: ", ticks_per_quarter_note, 1)
	#else:
		print_if_verbose( "Negative two's compliment of ", int(division[1:2], 16) - 128, "frames / second")
		print_if_verbose( int(data[fp:fp+2],16), "ticks / frame")
		song.timed = True
	fp += 4
	song.set_ticks_per_quarter_note(ticks_per_quarter_note)
		
	print_if_verbose( "READ HEADER CHUNK OF SIZE ", fp, "RESTARTING fp at position ", fp)
>>>>>>> develop
	#read track chunks
	for i in range(0, num_tracks):
		'''READS EACH TRACK CHUNK'''

		total_delta_time = 0
		data = data[fp:]
		#check track chunk type
		print_bytes(data[0:8], "\"MTrk\"")
		if re.match(r'4d54726b', data) == None:
<<<<<<< HEAD
			raise error.MidiException("Track does not begin with \"MTrk\"", "at position", fp)
		fp = 8
		#get track length
		track_len = int(data[fp:fp+8], 16)
		print_bytes(data[fp:fp+8], "Track length:", track_len)
=======
			raise error.MidiException("Track does not begin with \"MTrk\" ", "at position ", fp)
		fp = 8
		#get track length
		track_len = int(data[fp:fp+8], 16)
		print_bytes(data[fp:fp+8], "Track length: ", track_len)
>>>>>>> develop
		track_len *= 2 #measure in nibbles, not bytes
		remaining_track_len = track_len
		fp += 8
		list_of_notes = []
<<<<<<< HEAD
=======
		i = 0
>>>>>>> develop

		'''READS EACH DELTA_TIME - EVENT PAIR IN THE TRACK'''

		last_event_type = None
		no_event_head = False
		data = data[fp:]
		fp = 0
<<<<<<< HEAD
		#print "RESET TRACK", i+1, "fp TO 0 AT BEGINNING OF TRACK DATA"
=======
		print_if_verbose( "RESET TRACK ", i+1, "fp TO 0 AT BEGINNING OF TRACK DATA")
>>>>>>> develop
		def print_data(data):
			'''pretty-prints the data bytes for all events in a track chunk
			'data' is a string of hex values representing the data of the track chunk
			'''
			data_string = ""
			index_string = ""
			x = 0
			l = 100
			for i in range(0, len(data)):
				data_string += data[i]
				if (i+1) % l == 0 or i == len(data)-1:
<<<<<<< HEAD
					#print data_string
=======
					print_if_verbose( data_string)#prints hex content of the file
>>>>>>> develop
					if i < 1000:
						for j in range(0,(l+3)/4):
							space = len(str(x+j*4))
							index_string += str(x+j*4)
							for z in range(0, 4-space):
								index_string += " "
					else:
						for j in range(0,(l+7)/8):
							space = len(str(x+j*8))
							index_string += str(x+j*8)
							for z in range(0, 8-space):
								index_string += " "
<<<<<<< HEAD
					#print index_string
=======
					print_if_verbose( index_string)#prints indexes to go along with the hex content of the file
>>>>>>> develop
					index_string = ""
					x += l
					data_string = ""
		print_data(data)
		global new_event_type
		new_event_type = False
		while remaining_track_len > 0:
			global num_events
			'''READS EACH EVENT'''
<<<<<<< HEAD
			#print "-------------------"
			#print "len(data):", len(data)
=======
			print_if_verbose( "-------------------")
			print_if_verbose("i = ",i)
>>>>>>> develop
			if len(data) - fp <= 6:
				if data[-6:] != 'ff2f00':
					raise error.MidiException("Track does not end with end_of_track meta event")
				else:
					break

			if remaining_track_len < 0:
				raise error.MidiException("Track length does not match up with length of track data")
			j = 0
			binary_value = ""
			while int(data[fp + j:fp + j + 2], 16) >= 128:
				binary_string = bin(int(data[fp + j: fp + j + 2], 16))[2:].zfill(8)
<<<<<<< HEAD
				#print binary_string
				binary_value += binary_string[1:8]
				j += 2
			binary_string = bin(int(data[fp + j: fp + j + 2], 16))[2:].zfill(8)
			#print binary_string
			binary_value += binary_string[1:8]
			delta_time = int(binary_value, 2)
			print_bytes(data[fp:fp+j+2], "Delta time:", delta_time)
			total_delta_time += delta_time
			#print "remaining_track_len:", remaining_track_len
			#TODO adjust time position
			advance(j+2)
			#print "fp after delta_time:", fp
			#if int(first_byte, 16) < 128:
				#raise error.MidiException("Unrecognized event at position", fp, ". Expected 0x80-0xFF, but got", data[fp:fp+2])
=======
				binary_value += binary_string[1:8]
				j += 2
			binary_string = bin(int(data[fp + j: fp + j + 2], 16))[2:].zfill(8)
			binary_value += binary_string[1:8]
			delta_time = int(binary_value, 2)
			print_bytes(data[fp:fp+j+2], "Delta time: ", delta_time)
			''' 
				From what I can tell, delta time is actually the amount of time (ticks) that pass before the next event (not since the last one). Therefore, to have correct note (and other event) start times, I have to add the delta time after creating the start time.
			'''
			start_ticks = total_delta_time
			total_delta_time += delta_time
			print_if_verbose("Total delta time: ", total_delta_time)
			print_if_verbose( "\t(Remaining_track_len: ", remaining_track_len, ")")

			#TODO adjust time position
			advance(j+2)
			print_if_verbose( "\t(fp after delta_time: ", fp, ")")
			#if int(first_byte, 16) < 128:
				#raise error.MidiException("Unrecognized event at position ", fp, ". Expected 0x80-0xFF, but got ", data[fp:fp+2])
>>>>>>> develop
			n1 = data[fp] #first nibble of this event's data
			n2 = data[fp+1] #second nibble of this event's data
			b2 = data[fp+2:fp+4] #second byte of this event's data
			b3 = data[fp+4:fp+6] #third byte of this event's data
<<<<<<< HEAD
			#print "This event type:", n1, n2, b2, b3
			temp_fp = fp

			def read_variable_length():
				i = 0
				binary_value = ""
				while int(data[fp + i:fp + i + 2], 16) >= 128:
					binary_string = bin(int(data[fp + i: fp + i + 2], 16))[2:].zfill(8)
					#print binary_string
=======
			print_if_verbose( "\t(This event type: ", n1, n2, b2, b3, ")")
			temp_fp = fp

			#TODO this isn't used??? how is it not used at all?
			def read_variable_length():
				i = 0
				binary_value = ""
				while int(data[fp + i:fp + i + 2], 16) >= 128:#reads one byte at a time; if first bit is 1, it continues
					binary_string = bin(int(data[fp + i: fp + i + 2], 16))[2:].zfill(8)
>>>>>>> develop
					binary_value += binary_string[1:8]
					i += 2
				binary_string = bin(int(data[fp + i: fp + i + 2], 16))[2:].zfill(8)
				binary_value += binary_string[1:8]
				length = int(binary_value, 2)
				advance(i+2)
<<<<<<< HEAD
				#print "Variable length:", length
				return length

			def read_note_off(x):

				global channel
				#check/set key/velocity
				warnings.warn("Note off event not fully implemented")
				if int(data[fp:fp+2], 16) > 127:
					raise error.MidiException("Invalid note key at position", fp, ". Expected 0x00-0x7f, but got", b2)
				key = int(data[fp+1:fp+3], 16)
				if int(data[fp+2:fp+4], 16) > 127:
					raise error.MidiException("Invalid note velocity at position", fp, ". Expected 0x00-0x7f, but got", b3)
				velocity = int(data[fp+2:fp+4], 16)
				#set channel
				if x == None:
					set_channel(int(data[fp], 16))
					print_bytes(data[fp-2:fp+4], "Note off c nn vv")
				else:
					print_bytes(data[fp:fp+4], "nn vv")
				#print "Channel:", channel
				#find note and 
					#if in list: create note object
					#else raise error: note ended that was not started
				#print "Pop Note Command at fp:", fp
				advance(4)#pop note event is 3 bytes long

			def read_note_on(x):

=======
				return length

			def read_note_off(x):
				print_if_verbose("Note off event")
				global channel
				#check/set key/velocity
				key = int(data[fp:fp+2], 16)
				velocity = int(data[fp+2:fp+4], 16)
				print_if_verbose("\tTurning off ", key)
				#set channel
				if x == None:
					set_channel(int(data[fp-1], 16) + 1)
					print_if_verbose("Event header:")
					print_bytes(data[fp-2:fp+4], "Note off c nn vv")
				else:
					print_if_verbose("Event header:")
					print_bytes(data[fp:fp+4], "nn vv")
				print_if_verbose( "\tChannel: ", channel)
				#if in list: create note object
				found = False
				print_if_verbose("\tNotes that are on: ", list_of_notes)
				for nt in list_of_notes: 
					#create note object
					print_if_verbose(nt[0], "=? ", key, " ", nt[1], "=? ", channel)
					if nt[0] == key and nt[1] == channel and not found:
						duration = total_delta_time - nt[2]
						start = start_ticks
						note = song.add_note(start_ticks, duration, key, channel)
						print_if_verbose( "Note created: ", note.to_string(ticks_per_quarter_note))
						notes[channel].append(note)
						found = True
						list_of_notes.remove(nt) #remove from list_of_notes
						print_if_verbose("\tNotes that are on: ", list_of_notes)
					print_if_verbose("found: ", found)
				if not found:
					raise error.MidiException("Invalid note off event at position ", fp, ". No such note of pitch ", key, "is currently on")
				print_if_verbose( "Add/Pop Note Command at fp: ", fp)
				advance(4)#add note event is 3 bytes long
				print_if_verbose("\tNotes that are on: ", list_of_notes)

			def read_note_on(x):
				print_if_verbose("Note on event")
>>>>>>> develop
				global channel
				#check/set key/velocity
				key = int(data[fp:fp+2], 16)
				velocity = int(data[fp+2:fp+4], 16)
				#set channel
				if x == None:
					set_channel(int(data[fp-1], 16) + 1)
<<<<<<< HEAD
					print_bytes(data[fp-2:fp+4], "Note off c nn vv")
				else:
					print_bytes(data[fp:fp+4], "nn vv")
				#print "Channel:", channel
				note_tuple = (key, channel, total_delta_time)
=======
					print_if_verbose("Event header:")
					print_bytes(data[fp-2:fp+4], "Note on c nn vv")
				else:
					print_if_verbose("Event header:")
					print_bytes(data[fp:fp+4], "nn vv")
				print_if_verbose( "\tChannel: ", channel)
				note_tuple = (key, channel, start_ticks)
				found = False
>>>>>>> develop
				if velocity == 0:
					#if in list: create note object
					for nt in list_of_notes: 
						#create note object
<<<<<<< HEAD
						found = False
						if nt[0] == key and nt[1] == channel:
							duration = total_delta_time - nt[2]
							note = Note.Note(total_delta_time, duration, key, channel)
							#print "Note created:", note.to_string(ticks_per_quarter_note)
							notes[channel].append(note)
							found = True
							list_of_notes.remove(nt) #remove from list_of_notes
					#if not found:
						#print "Note created with velocity of 0 at position"
				else:
					#add note to list
					list_of_notes.append(note_tuple)
				#print "Add/Pop Note Command at fp:", fp
				advance(4)#add note event is 3 bytes long
=======
						if nt[0] == key and nt[1] == channel and not found:
							duration = total_delta_time - nt[2]
							note = song.add_note(start_ticks, duration, key, channel)
							print_if_verbose( "Note created: ", note.to_string(ticks_per_quarter_note))
							notes[channel].append(note)
							found = True
							print_if_verbose("\tTurning off ", key)
							list_of_notes.remove(nt) #remove from list_of_notes
							print_if_verbose("\tNotes that are on: ", list_of_notes)
					print_if_verbose("found: ", found)
					if not found:
						print_if_verbose( "Note created with velocity of 0 at position")
				else:
					#add note to list
					print_if_verbose("\tTurning on ", key)
					print_if_verbose("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
					list_of_notes.append(note_tuple)
					print_if_verbose("\tNotes that are on: ", list_of_notes)
				print_if_verbose( "Add/Pop Note Command at fp: ", fp)
				advance(4)#add note event is 3 bytes long
				print_if_verbose("\tNotes that are on: ", list_of_notes)
>>>>>>> develop

			def read_polyphonic():

				#check/set key/velocity
				#set channel
				#send message
<<<<<<< HEAD
				#print "Polyphonic Note at fp:", fp
=======
				print_if_verbose( "Polyphonic Note at fp: ", fp)
>>>>>>> develop
				advance(4)#polyphonic note event is 3 bytes long

			def read_control_change():

				#check control#, control_val
				#send message
<<<<<<< HEAD
				#print "Control Change at fp:", fp
=======
				print_if_verbose( "Control Change at fp: ", fp)
>>>>>>> develop
				print_bytes(data[fp:fp+4], "Control change")
				advance(4)#control change event is 3 bytes long

			def read_program_change():

				#check new_program_#
				#send message
<<<<<<< HEAD
				#print "Program Change at fp:", fp
				print_bytes(data[fp-2:fp+2], "Program change to", int(data[fp:fp+2], 16))
=======
				print_if_verbose( "Program Change at fp: ", fp)
				print_bytes(data[fp-2:fp+2], "Program change to ", int(data[fp:fp+2], 16))
>>>>>>> develop
				advance(2)#program change event is 2 bytes long

			def read_channel_key_pressure():

				#check channel_pressure_val
				#send message
<<<<<<< HEAD
				#print "Channel Key Pressure of", data[fp:fp+2], "at fp:", fp
=======
				print_if_verbose( "Channel Key Pressure of ", data[fp:fp+2], "at fp: ", fp)
>>>>>>> develop
				advance(2)#channel key pressure event is 2 bytes long

			def read_pitch_bend():

				#check msb, lsb
				#send message
<<<<<<< HEAD
				#print "Pitch Bend at fp:", fp
				advance(4)#pitch bend event is 3 bytes long



			def read_sysex():
				raise error.MidiException("Sysex event found at position", fp, "(sysex events not yet handled in program)")



			def read_sequence_number():
				warnings.warn("Sequence Number meta event found at position", fp, "(Sequence Number meta events not yet handled in program)")

			def read_text():
				raise error.MidiException("Text meta event found at position", fp, "(Text meta events not yet handled in program)")

			def read_copyright_notice():
				warnings.warn("Copyright notice meta event found at position", fp, "(Copyright notice meta events not yet handled in program)")

			def read_sequence_track_name():
				warnings.warn("Sequence/Track Name meta event found at position", fp, "(Sequence/Track Name meta events not yet handled in program)")

			def read_instrument_name():
				warnings.warn("Instrument Name meta event found at position", fp, "(Instrument Name meta events not yet handled in program)")

			def read_lyric():
				raise error.MidiException("Lyric meta event found at position", fp, "(Lyric meta events not yet handled in program)")

			def read_marker():
				raise error.MidiException("Marker meta event found at position", fp, "(Marker meta events not yet handled in program)")

			def read_cue():
				raise error.MidiException("Cue meta event found at position", fp, "(Cue meta events not yet handled in program)")

			def read_program_name():
				#print "Program name meta event read at position", fp
				length = 2 * (int(data[fp:fp+2], 16))
				program_name = data[fp:fp+length]
				advance(length+2)
				return program_name
				#raise error.MidiException("Program Name meta event found at position", fp, "(Program Name meta events not yet handled in program)")

			def read_midi_channel_prefix():
				if data[fp:fp+2] != '11':
					raise error.MidiException("Invalid MIDI Channel Prefix meta event found at position", fp, "(expected '11' but got", data[fp:fp+2],")")
				elif int(data[fp+2:fp+4], 16) > 15:
					raise error.MidiException("Invalid MIDI Channel Prefix meta event found at position", fp+2, "(expected 00-0f but got", data[fp+2:fp+4],")")
				else:
					set_channel(data[fp+2:fp+4] + 1)
=======
				print_if_verbose( "Pitch Bend at fp: ", fp)
				advance(4)#pitch bend event is 3 bytes long

			def read_sysex():
				raise error.MidiException("Sysex event found at position ", fp, "(sysex events not yet handled in program)")

			def read_sequence_number():
				raise error.MidiException("Sequence Number meta event found at position ", fp, "(Sequence Number meta events not yet handled in program)")

			def read_copyright_notice():
				raise error.MidiException("Copyright notice meta event found at position ", fp, "(Copyright notice meta events not yet handled in program)")

			def read_sequence_track_name():
				raise error.MidiException("Sequence/Track Name meta event found at position ", fp, "(Sequence/Track Name meta events not yet handled in program)")

			def read_lyric():
				raise error.MidiException("Lyric meta event found at position ", fp, "(Lyric meta events not yet handled in program)")

			def read_marker():
				raise error.MidiException("Marker meta event found at position ", fp, "(Marker meta events not yet handled in program)")

			def read_cue():
				raise error.MidiException("Cue meta event found at position ", fp, "(Cue meta events not yet handled in program)")

			def get_text(nibbles = 2):
				length = read_variable_length()
				number_of_data_nibbles = length * 2
				# length = 2 * (int(data[fp:fp+2], 16))
				text = data[fp:fp + number_of_data_nibbles]
				advance(number_of_data_nibbles)
				# advance(length+nibbles)
				return text
				#raise error.MidiException("Program Name meta event found at position ", fp, "(Program Name meta events not yet handled in program)")

			def read_midi_channel_prefix():
				if data[fp:fp+2] != '01':
					raise error.MidiException("Invalid MIDI Channel Prefix meta event found at position ", fp, "(expected '11' but got ", data[fp:fp+2],")")
				elif int(data[fp+2:fp+4], 16) > 15:
					raise error.MidiException("Invalid MIDI Channel Prefix meta event found at position ", fp+2, "(expected 00-0f but got ", data[fp+2:fp+4],")")
				else:
					set_channel(int(data[fp+2:fp+4], 16) + 1)
>>>>>>> develop
					advance(4)
					return channel

			def read_midi_port():
				if data[fp:fp+2] != '01':
<<<<<<< HEAD
					raise error.MidiException("Invalid MIDI Port meta event found at position", fp, "(expected '01' but got", data[fp:fp+2],")")
=======
					raise error.MidiException("Invalid MIDI Port meta event found at position ", fp, "(expected '01' but got ", data[fp:fp+2],")")
>>>>>>> develop
				else:
					port = int(data[fp+2:fp+4], 16) + 1
					advance(4)
					return port

			def read_end_of_track():
				if data[fp:fp+2] == '00':
<<<<<<< HEAD
					#print "********************YAAAAAAY********************"
					advance(2)
				else:
					raise error.MidiException("Unrecognized End of Track meta event found at position", fp, "found", data[fp:fp+2], "but expected 0x00")

			def read_tempo():
				if data[fp:fp+2] != "03":
					raise error.MidiException("Unrecognized Set Tempo meta event at position", fp, "found", data[fp:fp+2], "but expected 0x03")
				else:
					mpq = int(data[fp+2:fp+8], 16)

				#print "Tempo set to", mpq, "microseconds per quarter note", "(", 60000000/mpq, " beats per minute)"
				advance(8)

			def read_SMTPE_offset():
				raise error.MidiException("SMTPE Offset meta event found at position", fp, "(SMTPE Offset meta events not yet handled in program)")

			def read_time_signature():
				if data[fp:fp+2] != "04":
					raise error.MidiException("Unrecognized Time Signature meta event at position", fp, "found", data[fp+4:fp+6], "but expected 0x04")
=======
					print_if_verbose( "********************YAAAAAAY********************")
					advance(2)
				else:
					raise error.MidiException("Unrecognized End of Track meta event found at position ", fp, "found ", data[fp:fp+2], "but expected 0x00")

			def read_tempo():
				if data[fp:fp+2] != "03":
					raise error.MidiException("Unrecognized Set Tempo meta event at position ", fp, "found ", data[fp:fp+2], "but expected 0x03")
				else:
					mpq = int(data[fp+2:fp+8], 16)

				print_if_verbose( "Tempo set to ", mpq, "microseconds per quarter note ", "( ", 60000000/mpq, " beats per minute)")
				advance(8)

			def read_SMTPE_offset():
				raise error.MidiException("SMTPE Offset meta event found at position ", fp, "(SMTPE Offset meta events not yet handled in program)")

			def read_time_signature():
				if data[fp:fp+2] != "04":
					raise error.MidiException("Unrecognized Time Signature meta event at position ", fp, "found ", data[fp+4:fp+6], "but expected 0x04")
>>>>>>> develop
				else:
					numerator = int(data[fp+2:fp+4], 16)
					denominator = 2 ** int(data[fp+4:fp+6], 16)
					cpmt = int(data[fp+6:fp+8], 16)
					nonp = int(data[fp+8:fp+10], 16)
					time_sig = str(numerator) + "/" + str(denominator)
					song.set_time_sig(time_sig)
<<<<<<< HEAD
					#print "Time signature:", numerator, "/", denominator
=======
					print_if_verbose( "Time signature: ", numerator, "/ ", denominator)
>>>>>>> develop
				advance(10)

			def read_key_signature():
				if data[fp:fp+2] != "02":
<<<<<<< HEAD
					raise error.MidiException("Unrecognized Key Signature meta event at position", fp, "found", data[fp+4:fp+6], "but expected 0x02")
				else:
					numsharps = int(data[fp+2:fp+4], 16)
					mode = data[fp+4:fp+6]
					majorkeys = {	249 : "C flat major",
									250 : "G flat major",
									251 : "D flat major",
									252 : "A flat major",
									253 : "E flat major",
									254 : "B flat major",
									255 : "F major",
									0  : "C major",
									1  : "G major",
									2  : "D major",
									3  : "A major",
									4  : "E major",
									5  : "B major",
									6  : "F sharp major",
									7  : "C sharp major"}
					minorkeys = {	5  : "C flat minor",
									6  : "G flat minor",
									7  : "D flat minor",
									249 : "A flat minor",
									250 : "E flat minor",
									251 : "B flat minor",
									252 : "F minor",
									253 : "C minor",
									254 : "G minor",
									255 : "D minor",
									0  : "A minor",
									1  : "E minor",
									2  : "B minor",
									3  : "F sharp minor",
									4  : "C sharp minor"}
					if mode == "00":
						song.set_key(majorkeys[numsharps])
						#print "Key signature:", majorkeys[numsharps]
					else:
						song.set_key(minorkeys[numsharps])
						#print "Key signature:", minorkeys[numsharps]
				advance(6)

			def read_sequence_specific():
				raise error.MidiException("Sequencer-Specific meta event found at position", fp, "(Sequencer-Specific meta events not yet handled in program)")

			def determine_event(x):
				#print "x:", x
				#if x == None:
					#print "fp:", fp
				global new_event_type, n1, n2, b2, b3
				if x == None:
					new_event_type = True
				#print "new_event_type:", new_event_type
=======
					raise error.MidiException("Unrecognized Key Signature meta event at position ", fp, "found ", data[fp+4:fp+6], "but expected 0x02")
				else:
					numsharps = int(data[fp+2:fp+4], 16)
					mode = data[fp+4:fp+6]
					majorkeys = {	249 : "C flat major ",
									250 : "G flat major ",
									251 : "D flat major ",
									252 : "A flat major ",
									253 : "E flat major ",
									254 : "B flat major ",
									255 : "F major ",
									0  : "C major ",
									1  : "G major ",
									2  : "D major ",
									3  : "A major ",
									4  : "E major ",
									5  : "B major ",
									6  : "F sharp major ",
									7  : "C sharp major"}
					minorkeys = {	5  : "C flat minor ",
									6  : "G flat minor ",
									7  : "D flat minor ",
									249 : "A flat minor ",
									250 : "E flat minor ",
									251 : "B flat minor ",
									252 : "F minor ",
									253 : "C minor ",
									254 : "G minor ",
									255 : "D minor ",
									0  : "A minor ",
									1  : "E minor ",
									2  : "B minor ",
									3  : "F sharp minor ",
									4  : "C sharp minor"}
					if mode == "00":
						song.set_key(majorkeys[numsharps])
						print_if_verbose( "Key signature: ", majorkeys[numsharps])
					else:
						song.set_key(minorkeys[numsharps])
						print_if_verbose( "Key signature: ", minorkeys[numsharps])
				advance(6)

			def determine_event(x):
				print_if_verbose( "\tEvent type: ", x)
				if x == None:
					print_if_verbose( "\t(fp: ", fp, ")")
				global new_event_type, n1, n2, b2, b3
				if x == None:
					new_event_type = True
>>>>>>> develop
				'''HANDLE MIDI EVENTS'''
				if n1 == '8':
					#pop note command
					if x == None:
						advance(2)
					read_note_off(x)
				elif n1 == '9':
					#add/pop note command
					if x == None:
						advance(2)
					read_note_on(x)
				elif n1 == 'a':
					#polyphonic note
					if x == None:
						advance(2)
					read_polyphonic()
				elif n1 == 'b':

					#MIDI Channel Mode Messages
					if b2 == '78':
						print_bytes(data[fp:fp+6], "All Sound Off")
						advance(6)
					elif b2 == '79':
						print_bytes(data[fp:fp+6], "Reset All Controllers")
						advance(6)
					elif b2 == '7a':
						print_bytes(data[fp:fp+6], "Local Control")
						advance(6)
					elif b2 == '7b':
						print_bytes(data[fp:fp+6], "All Notes Off")
						advance(6)
					elif b2 == '7c':
						print_bytes(data[fp:fp+6], "Omni Mode Off")
						advance(6)
					elif b2 == '7d':
						print_bytes(data[fp:fp+6], "Omni Mode On")
						advance(6)
					elif b2 == '7e':
						print_bytes(data[fp:fp+6], "Mono Mode On")
						advance(6)
					elif b2 == '7f':
						print_bytes(data[fp:fp+6], "Poly Mode On")
						advance(6)
					else:
						#control change
						if x == None:
							advance(2)
						read_control_change()
				elif n1 == 'c':
					#program change
					if x == None:
						advance(2)
					read_program_change()
				elif n1 == 'd':
					#channel key pressure
					if x == None:
						advance(2)
					read_channel_key_pressure()
				elif n1 == 'e':
					#pitch bend
					if x == None:
						advance(2)
					read_pitch_bend()
				elif n1 == 'f':

					'''HANDLE SYSEX EVENTS'''
					if n2 == 0:
						if x == None:
							advance(2)
						read_sysex()
					elif n2 == 7:
						if x == None:
							advance(2)
						read_sysex()
					elif n2 == 'f':
						'''HANDLE META EVENTS'''
						if b2 == '00':
							if x == None:
								advance(4)
							read_sequence_number()
						elif b2 == '01':
<<<<<<< HEAD
							if x == None:
								advance(4)
							read_text()
=======
							#Composer Name
							#THIS IS NOT ON THE INTERNET FOR SOME REASON BUT IT'S A FREAKING THING AND I HAD TO FIGURE IT OUT FOR MYSELF
							if x == None:
								advance(4)
							print_if_verbose( "Composer meta event read at position ", fp)
							composer_name = get_text().decode("hex")
							print_if_verbose( "Composer Name: ", composer_name)
							print_if_verbose( "fp is now: ", fp)
>>>>>>> develop
						elif b2 == '02':
							#Copyright notice
							if x == None:
								advance(4)
							read_copyright_notice()
						elif b2 == '03':
							#Sequence/Track Name
							if x == None:
								advance(4)
<<<<<<< HEAD
							read_sequence_track_name()
=======
							#read_sequence_track_name()
							print_if_verbose( "Sequence/Track Name meta event read at position ", fp)
							seq_track_name = get_text().decode("hex")
							print_if_verbose( "Sequence/Track Name: ", seq_track_name)
							print_if_verbose( "fp is now: ", fp)
>>>>>>> develop
						elif b2 == '04':
							#Instrument Name
							if x == None:
								advance(4)
<<<<<<< HEAD
							read_instrument_name()
=======
							print_if_verbose( "Instrument Name meta event read at position ", fp)
							instrument_name = get_text().decode("hex")
							print_if_verbose( "Instrument Name: ", instrument_name)
							print_if_verbose( "fp is now: ", fp)
>>>>>>> develop
						elif b2 == '05':
							#Lyric
							if x == None:
								advance(4)
							read_lyric()
						elif b2 == '06':
							#Marker
							if x == None:
								advance(4)
							read_marker()
						elif b2 == '07':
							#Cue Point
							if x == None:
								advance(4)
							read_cue()
						elif b2 == '08':
							#Program Name
							if x == None:
								advance(4)
<<<<<<< HEAD
							name_hex = read_program_name()
							program_name = name_hex.decode("hex")
							song.set_title(program_name)
							#print "Program Name:", program_name
							#print "fp is now:", fp
=======
							print_if_verbose( "Program Name meta event read at position ", fp)
							name_hex = get_text()
							program_name = name_hex.decode("hex")
							song.set_title(program_name)
							print_if_verbose( "Program Name: ", program_name)
							print_if_verbose( "fp is now: ", fp)
>>>>>>> develop
						elif b2 == '0a':
							#Composer Name
							#THIS IS NOT ON THE INTERNET FOR SOME REASON BUT IT'S A FREAKING THING AND I HAD TO FIGURE IT OUT FOR MYSELF
							if x == None:
								advance(4)
<<<<<<< HEAD
							program_name = read_program_name().decode("hex")
							#print "Composer Name:", program_name
							#print "fp is now:", fp
=======
							print_if_verbose( "Composer Name meta event read at position ", fp)
							program_name = get_text().decode("hex")
							print_if_verbose( "Composer Name: ", program_name)
							print_if_verbose( "fp is now: ", fp)
>>>>>>> develop
						elif b2 == '20':
							#MIDI Channel Prefix
							if x == None:
								advance(4)
							set_channel(read_midi_channel_prefix())
<<<<<<< HEAD
							#print "MIDI channel set to", channel
=======
							print_if_verbose( "MIDI channel set to ", channel)
>>>>>>> develop
						elif b2 == '21':
							#MIDI Port
							if x == None:
								advance(4)
							port = read_midi_port()
<<<<<<< HEAD
							#print "MIDI port set to port", port
=======
							print_if_verbose( "MIDI port set to port ", port)
>>>>>>> develop
						elif b2 == '2f':
							#End of Track
							if x == None:
								advance(4)
							read_end_of_track()
						elif b2 == '51':
							#Set Tempo
							if x == None:
								advance(4)
							read_tempo()
						elif b2 == '54':
							#SMTPE Offset
							if x == None:
								advance(4)
							read_SMTPE_offset()
						elif b2 == '58':
							#Time Signature
							if x == None:
								advance(4)
							read_time_signature()
						elif b2 == '59':
							#Key Signature
							if x == None:
								advance(4)
							read_key_signature()
						elif b2 == '7f':
							#Sequencer-Specific
<<<<<<< HEAD
							if x == None:
								advance(4)
							read_sequence_specific()
						else:
							if x != None:
								raise error.MidiException("Unrecognized Meta event at position", fp, ". Expected 00-08, 20, 2f, 51, 54, 58, 59, or 7f, but got", b2)
							n1 = last_event_type[:1]
							n2 = last_event_type[1:2]
							b2 = last_event_type[2:4]
							'''print "n1:", n1
							print "n2:", n2
							print "b2:", b2'''
							#print "Using last header (", last_event_type, ") because none identified at", fp
=======
							print_if_verbose( "Sequence-Specific meta event read at position ", fp)
							if x == None:
								advance(4)
							#read_sequence_specific()
							variable_length_value = read_variable_length()
							number_of_data_nibbles = variable_length_value * 2

							program_name = get_text(number_of_data_nibbles).decode("hex")
							print_if_verbose( "Sequence-Specific: ", program_name)
							print_if_verbose( "fp is now: ", fp)
						elif b2 == '4b':
							raise error.MidiException("M-Live Tag event not yet dealt with. Please visit https://www.mixagesoftware.com/en/midikit/help/HTML/meta_events.html")
						else:
							if x != None:
								raise error.MidiException("Unrecognized Meta event at position ", fp, ". Expected 00-08, 20, 2f, 51, 54, 58, 59, or 7f, but got ", b2)
							n1 = last_event_type[:1]
							n2 = last_event_type[1:2]
							b2 = last_event_type[2:4]
							'''print "n1: ", n1
							print "n2: ", n2
							print "b2: ", b2'''
							print_if_verbose( "\t(Using last header ( ", last_event_type, ") because none identified at ", fp, ")")
>>>>>>> develop
							new_event_type = False
							determine_event(last_event_type)
					else:
						if x != None:
<<<<<<< HEAD
							raise error.MidiException("Unrecognized event at position", fp, ". Expected 0x80-0xff, but got", data[fp:fp+2])
						n1 = last_event_type[:1]
						n2 = last_event_type[1:2]
						b2 = last_event_type[2:4]
						'''print "n1:", n1
						print "n2:", n2
						print "b2:", b2'''
						#print "Using last header (", last_event_type, ") because none identified at", fp
=======
							raise error.MidiException("Unrecognized event at position ", fp, ". Expected 0x80-0xff, but got ", data[fp:fp+2])
						n1 = last_event_type[:1]
						n2 = last_event_type[1:2]
						b2 = last_event_type[2:4]
						'''print "n1: ", n1
						print "n2: ", n2
						print "b2: ", b2'''
						print_if_verbose( "\tUsing last header ( ", last_event_type, ") because none identified at ", fp, ")")
>>>>>>> develop
						new_event_type = False
						determine_event(last_event_type)
				else:
					if x != None:
<<<<<<< HEAD
						raise error.MidiException("Unrecognized event at position", fp, ". Expected 0x80-0xff, but got", data[fp:fp+2])
					n1 = last_event_type[:1]
					n2 = last_event_type[1:2]
					b2 = last_event_type[2:4]
					'''print "n1:", n1
					print "n2:", n2
					print "b2:", b2'''
					#print "Using last header (", last_event_type, ") because none identified at", fp
=======
						raise error.MidiException("Unrecognized event at position ", fp, ". Expected 0x80-0xff, but got ", data[fp:fp+2])
					n1 = last_event_type[:1]
					n2 = last_event_type[1:2]
					b2 = last_event_type[2:4]
					'''print "n1: ", n1
					print "n2: ", n2
					print "b2: ", b2'''
					print_if_verbose( "\tUsing last header ( ", last_event_type, ") because none identified at ", fp, ")")
>>>>>>> develop
					new_event_type = False
					determine_event(last_event_type)
			determine_event(None)
			num_events += 1
			if new_event_type:
				last_event_type = data[temp_fp:temp_fp+6]
<<<<<<< HEAD
	song.num_events = num_events
	#print file_name, "is a valid MIDI file."
	number_of_notes = 0
	for c in notes:
		for n in notes[c]:
			number_of_notes += 1
			#print n.to_string(ticks_per_quarter_note)
	#print "Number of notes in file:", number_of_notes
=======
	song.set_num_events(num_events)
	print_if_verbose( file_name, "is a valid MIDI file.")
	number_of_notes = 0
	#print_if_verbose("&&& Notes: ", notes)
	note_list = []
	for c in notes:
		for n in notes[c]:
			note_list.append(n)
			number_of_notes += 1
			#print_if_verbose( n.to_string(ticks_per_quarter_note))
	print_if_verbose( "Number of notes in file: ", number_of_notes)
	song.set_notes(notes)
>>>>>>> develop
	song.set_num_channels(len(channels))
	return song

