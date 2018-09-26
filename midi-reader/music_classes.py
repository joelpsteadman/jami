#Music Classes
import math

class Song:
	title = "Not set"
	num_tracks = "Not set"
	num_channels = "Not set" #might not need
	num_events = "Not set"
	key = "Not set"
	time_sig = ""
	ticks_per_quarter_note = ""
	notes = []

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
		s += "\nnotes: "
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

	def __init__(self, start, duration, pitch, channel):
		self.pitch = pitch
		self.start = start
		self.duration = duration
		self.channel = channel

	#TODO instead of converting ticks to rhythm here, do it in the midi_reader file
	def to_string(self, ticks_per_quarter_note = None):
			def round_rhythm(time):
				frac, whole = math.modf(time)
				if frac > .9 or frac < .1:
					frac = 0.0
				elif frac > .2 and frac < .28:
					frac = 0.25
				elif frac > .29 and frac < .4:
					frac = 1/3
				elif frac > .45 and frac < .55:
					frac = 0.5
				elif frac > .56 and frac < .7:
					frac = 2/3
				elif frac > .7 and frac < .8:
					frac = 0.75
				print "\nRounded rythm: ", whole+frac
				return whole+frac
			notes = {	0 : 'C',
						1 : 'C#',
						2 : 'D',
						3 : 'D#',
						4 : 'E',
						5 : 'F',
						6 : 'F#',
						7 : 'G',
						8 : 'G#',
						9 : 'A',
						10: 'A#',
						11: 'B',
						}
			string = ""
			note = str(notes[self.pitch % 12]) + str(self.pitch / 12 + 1)
			if ticks_per_quarter_note == None:
				string = "Channel: "
				string += self.channel, "Pitch:", self.pitch, "start:", self.start*960, "seconds", "Duration:", self.duration*960, "seconds"
			else:
				string = "Channel: "
				string += str(self.channel) + ", Pitch: " + note + ", start: " + str(round_rhythm(self.start / float(ticks_per_quarter_note))) + " quarter notes, Duration: " + str(round_rhythm(self.duration / float(ticks_per_quarter_note))) + " quarter notes"
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