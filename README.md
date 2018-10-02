# jami
Joel's Artificial Music Intelligence for reading and writing music using MIDI files

MIDI-READER:

	GOAL:
	Create a Python program that can take a MIDI file as input and translate it into readable Python objects

	HOW TO RUN:
	1) Download this repository
	2) Navigate into the midi-reader folder on a terminal application with Python 2.7 installed (before running, it is a good idea to clear your console window)
	3) Run the following line to create an object that represents Air_on_the_G_String.mid and to print out info about this file:
	python test.py Air_on_the_G_String.mid

	You can also add -v or -verbose to the end to print debugging info about the midi file reading process*:
	python test.py Air_on_the_G_String.mid -v

	Run this line to run the old version of the code*:
	python output_midi_data.py Air_on_the_G_String.mid

	The syntax for a command to read MIDI files is:
	python test.py [file_path]+ [-v | -verbose]?

	*this will dump a ton of information about the midi file into the console window

MIDI-WRITER:
