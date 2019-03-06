#Music Classes
import math

class Song:
	title = "Not set"
	num_tracks = "Not set"
	num_channels = "Not set" #might not need
	num_events = "Not set"
	key = "Not set"
	time_sig = ""
	ticks_per_quarter_note = None
	notes = []
	timed = False #if true, file works by timing in ticks, rather than rhythmic notation

	def __init__(self):
		self.title = "Not set"

	def __str__(self):
		s = "title: "
		s += str(self.title)
		s += "\nnum_tracks: "
		s += str(self.num_tracks)
		s += "\nnum_channels: "
		s += str(self.num_channels)
		s += "\nnum_events: "
		s += str(self.num_events)
		s += "\nkey: "
		s += str(self.key)
		s += "\ntime_sig: "
		s += str(self.time_sig)
		s += "\nnotes: \n"
		for channel in self.notes:
			for note in self.notes[channel]:
				s += note.to_string(self.ticks_per_quarter_note)
				s += "\n"
		return s

	def set_title(self, title):
		self.title = title

	def set_num_tracks(self, num):
		self.num_tracks = num

	def set_num_channels(self, num):
		self.num_channels = num

	def set_num_events(self, num):
		self.num_events = num

	def set_key(self, key):
		self.key = key

	def set_time_sig(self, time):
		self.time_sig = time

	def set_ticks_per_quarter_note(self, val):
		self.ticks_per_quarter_note = val

	def set_notes(self, notes):
		self.notes = notes

	def add_to_db(self):
		return None

	def add_note(self, start, duration, pitch, channel):
		note = self.Note(start, duration, pitch, channel, self.ticks_per_quarter_note)
		return note

	class Note:
		pitch = 0
		start = 0.0
		duration = 0.0
		channel = 0

		def __init__(self):
			self.pitch = 0
			self.start = 0
			self.duration = 0
			self.channel = 0

		def __init__(self, start, duration, pitch, channel, ticks_per_quarter_note = None):
			def round_rhythm(time):
					frac, whole = math.modf(time)
					print "\tTime: ", time, "Fraction: ", frac, "Whole: ", whole
					if  frac < .1:
						frac = 0.0
						print "\tfrac < .1 so frac is being rounded to 0.0"
					elif frac > .9:
						whole += 1
						frac = 0.0
						print "\tfrac > .9 so frac is being rounded to 0.0 and 1 is being added to whole"
					elif frac > .2 and frac < .28:
						frac = 0.25
						# print "\nfrac > .2 -> frac := 0.25"
					elif frac > .29 and frac < .4:
						frac = 1.0/3.0
						# print "\nfrac > .29 -> frac := "
					elif frac > .45 and frac < .55:
						frac = 0.5
						# print "\nfrac > .2 -> frac := 0.25"
					elif frac > .56 and frac < .7:
						frac = 2.0/3.0
						# print "\nfrac > .2 -> frac := 0.25"
					elif frac > .7 and frac < .8:
						frac = 0.75
						# print "\nfrac > .2 -> frac := 0.25"
					else:
						print "!!!!!!!!!!"
					print "\tRounded rhythm: ", whole, " + ", frac, " = ", whole+frac
					return whole+frac
			self.pitch = pitch
			self.channel = channel
			if ticks_per_quarter_note == None:
				self.start = start*960
				self.duration = duration*960
			else:
				# print "\t+++", start % 480, "ticks -> ", (round_rhythm(start / float(ticks_per_quarter_note))), "beats"
				# print "\t+++", duration, "ticks -> ", (round_rhythm(duration / float(ticks_per_quarter_note))), "beats"
				self.start = round_rhythm(start / float(ticks_per_quarter_note))
				# print "{{{", duration, ticks_per_quarter_note, duration / float(ticks_per_quarter_note)
				print "\tStart ticks: ", start, " / ", ticks_per_quarter_note, "ticks/qtr-note = ", self.start, "qtr-notes"
				self.duration = round_rhythm(duration / float(ticks_per_quarter_note))
				print "\tDuration ticks: ", duration, " / ", ticks_per_quarter_note, "ticks/qtr-note = ", self.duration, "qtr-notes"
				

		#TODO instead of converting ticks to rhythm here, do it in the midi_reader file
		def to_string(self, ticks_per_quarter_note = None):
				#TODO make sharps an option
				notes = {	0 : 'C',
							1 : 'Db',
							2 : 'D',
							3 : 'Eb',
							4 : 'E',
							5 : 'F',
							6 : 'Gb',
							7 : 'G',
							8 : 'Ab',
							9 : 'A',
							10: 'Bb',
							11: 'B',
							}
				string = ""
				note = str(notes[self.pitch % 12]) + str(self.pitch / 12 + 1)
				# if ticks_per_quarter_note == None:
				# 	string = "Channel: "
				# 	string += self.channel, "Pitch:", self.pitch, "start:", self.start*960, "seconds", "Duration:", self.duration*960, "seconds"
				# else:
				# 	string = "Channel: "
				# 	string += str(self.channel) + ", Pitch: " + note + ", start: " + str(round_rhythm(self.start / float(ticks_per_quarter_note))) + " quarter notes, Duration: " + str(round_rhythm(self.duration / float(ticks_per_quarter_note))) + " quarter notes"
				
				if ticks_per_quarter_note == None:
					string = "Channel: "
					string += self.channel, "Pitch:", self.pitch, "start:", self.start*960, "seconds", "Duration:", self.duration*960, "seconds"
				else:
					string = "Channel: "
					string += str(self.channel) + ", Pitch: " + note + ", start: " + str(round(self.start, 2)) + " quarter notes, Duration: " + str(round(self.duration, 2)) + " quarter notes"
				return string
				
		def overlap(self, note):
			a = self.start
			b = self.start + self.duration
			x = note.start
			y = note.start + note.duration

			if x >= b or a >=y:
				return 0
			elif a <= x and b <= y:
				return 2 * (b-x) / (self.duration + note.duration)
			elif a <= x and b >= y:
				return 2 * (note.duration) / (self.duration + note.duration)
			elif a >= x and b <= y:
				return 2 * (y-a) / (self.duration + note.duration)
			elif a >= x and b >= y:
				return 2 * (self.duration) / (self.duration + note.duration)