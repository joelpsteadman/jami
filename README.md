# jami
Joel's Artificial Music Intelligence for reading and writing music using MIDI files

ARTIFICIAL INTELLIGENCE:

	GOAL:
	Create a Python program that can create new music based on patterns found in existing music.

	HOW TO RUN:
	In the ai/ directory, run python setup.py install to get the imported Python MIDI library working.
	In the ai/tests/ directory, run python JAMI.py to start up the AI application.

	IMPORTANT:
	Music files to be scanned sor the database should be placed in the ai/tests/m/ directory.
	
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

GENERAL:
	The goal of this project is to enjoy coding and do so in a way that it helpful to me professionally and to the community in a meaningful way:
	IDEAS:
		Write this in Python and Java and maybe a few other languages that I want to get aquainted with: R, Go, etc.
		Use frameworks and technologies like MAVEN and AWS
		Read MIDI files and change their formats. 
		Analyze MIDI and music XML files based on music theory rules
