#Music Classes

class Song:
	title = "Not set"
	num_tracks = "Not set"
	num_channels = "Not set" #might not need
	num_events = "Not set"
	key = "Not set"
	time_sig = ""
	notes = []

	def __init__(self):
		self.num_tracks = 0

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

	def set_notes(self, notes):
		self.num_tracks = notes

class Note:
	pitch = 0
	start = 0.0
	duration = 0.0
	channel = 0
	def __init__(self):
		self.pitch = 0
		self.start = 0
		self.end = 0
		self.channel = 0
	def __init__(self, pitch, start, end, channel):
		self.pitch = pitch
		self.start = start
		self.end = end
		self.channel = channel

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