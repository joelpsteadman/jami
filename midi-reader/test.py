#test.py
import sys
import music_classes
import midi
import midi_reader

v = False
f = sys.argv[1]
if len(sys.argv) > 2:
    if sys.argv[2] == "-verbose" or sys.argv[2] == "-v":
        print "VERBOSE"
        v = True

song = midi_reader.get_info(f, v)
#song = music_classes.Song("Air_on_the_G_String.mid")

print song