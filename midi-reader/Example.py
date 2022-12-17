import sys

from MIDI_Reader import MIDI_Reader
import Tools.Global_Variables as const

# TODO allow for -h, --help. Also display help if syntax is entered incorrectly

file_paths = list()
argument_index = 1
if len(sys.argv) > 1:
    file_paths.append(sys.argv[argument_index])
argument_index += 1
done = False
while len(sys.argv) > argument_index and not done:
    if sys.argv[argument_index] == "-verbose" or sys.argv[argument_index] == "-v":
        print("VERBOSE")
        const.VERBOSE = True
        done = True
    else:
        file_paths.append(sys.argv[argument_index])
        argument_index += 1
        
const.VERBOSE = True # TODO temporary workaround for debugging with VSCode

i = 1
if len(file_paths) == 0:
    file_paths.append("/Users/joelbreit/Documents/Code/MIDI/python-midi/JAMI/MIDI-Reader/Air_on_the_G_String.mid") # TODO only a local solution
for file_path in file_paths:
    reader = MIDI_Reader(file_path)
    song = reader.create_song()
    print(song)
