#test.py
import music_classes
import midi
import midi_reader

song = midi_reader.get_info("Air_on_the_G_String.mid")
#song = music_classes.Song("Air_on_the_G_String.mid")

print song