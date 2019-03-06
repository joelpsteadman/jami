#test.py
import sys
import music_classes
import midi
import midi_reader

v = False
files = list()
argument_index = 1
files.append(sys.argv[argument_index])
argument_index += 1
done = False
while len(sys.argv) > argument_index and not done:
    if sys.argv[argument_index] == "-verbose" or sys.argv[argument_index] == "-v":
        print "VERBOSE"
        v = True
        done = True
    else:
        files.append(sys.argv[argument_index])
        argument_index += 1

i = 1
for f in files:
    song = midi_reader.get_info(f, v)
    #song = music_classes.Song("Air_on_the_G_String.mid")
    print "Song #", i, ":"
    print song
    i += 1