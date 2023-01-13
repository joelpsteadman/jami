from Models.Note import Note

class Song:
	def __init__(self) -> None:
		self.title = "Not set"
		self.num_tracks = "Not set"
		self.num_channels = "Not set" #might not need
		self.num_events = 0
		self.key = "Not set"
		self.time_signature = "Not set"
		self.ticks_per_quarter_note = "Not set"
		self.notes = []
		self.timed = False #if true, file works by timing in ticks, rather than rhythmic notation

	def __str__(self):
		s = "Title: "
		s += str(self.title)
		s += "\nNumber of tracks: "
		s += str(self.num_tracks)
		s += "\nNumber of channels: "
		s += str(self.num_channels)
		s += "\nNumber of events: "
		s += str(self.num_events)
		s += "\nKey signature: "
		s += str(self.key)
		s += "\nTime signature: "
		s += str(self.time_signature)
		s += "\n"
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

	def set_time_signature(self, time):
		self.time_signature = time

	def set_ticks_per_quarter_note(self, val):
		self.ticks_per_quarter_note = val

	def set_notes(self, notes):
		self.notes = notes

	def add_to_db(self):
		return None

	def add_note(self, start, duration, pitch, channel):
		note = Note(start, duration, pitch, channel, self.ticks_per_quarter_note)
		return note