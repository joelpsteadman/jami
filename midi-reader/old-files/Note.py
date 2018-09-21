class Note:
	''' a class for musical notes within a MIDI file'''
	def __init__(self, pos, dur, pitch, channel):
		self.position = pos
		self.duration = dur
		self.pitch = pitch
		self.channel = channel

	def to_string(self, ticks_per_quarter_note = None):

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
			string = "Channel:"
			string += self.channel, "Pitch:", self.pitch, "Position:", self.position*960, "seconds", "Duration:", self.duration*960, "seconds"
		else:
			string = "Channel: "
			string += str(self.channel) + ", Pitch: " + note + ", Position: " + str(round(self.position / float(ticks_per_quarter_note), 1)) + " quarter notes, Duration: " + str(round(self.duration / float(ticks_per_quarter_note), 1)) + " quarter notes"
		return string

	def overlap(self, note):
		a = self.position
		b = self.position + self.duration
		x = note.position
		y = note.position + note.duration

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