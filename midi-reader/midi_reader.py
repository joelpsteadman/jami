import binascii
import codecs
import re as regex

from Models.Song import Song
from Tools.Logger import Logger
from Models.Events import Events
from Models.Event import Event
from Models.Events import event_names

class MIDI_Reader:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.song_object = Song()
        self.remaining_track_len = 0
        self.file_position = 0

        self.header_nibble_1 = ""
        self.header_nibble_2 = ""
        self.event_byte_2 = ""
        self.event_byte_3 = ""
        self.event_byte_4 = ""
        self.event = Event()

        self.read_file()

    def create_song(self):
        return self.song_object

    def read_file(self):
        if not self.file_path.endswith('.mid'):
            Logger.error(f"The file {self.file_path} is not a MIDI file. MIDI files must end with the .mid extension")

        with open(self.file_path, "rb") as file:
            byte_array = bytearray(file.read())
            # data_bytes = binascii.hexlify(byte_array)
            file_hex_str = byte_array.hex()

        channels = {}
        def set_channel(channel):
            channels[channel] = 1

        channel = 0
        notes = {} # a dictionary of 16 lists of Notes cooresponding to their channel number
        for i in range(0,16):
            key = i
            notes[key] = list()
            '''
            notes now has the form:
            notes{
                0: ()
                1: ()
                2: ()
                3: ()
                4: ()
                5: ()
                6: ()
                7: ()
                8: ()
                9: ()
                10: ()
                11: ()
                12: ()
                13: ()
                14: ()
                15: ()
            }
            '''

        # self.file_position = 0 # file_position
        self.remaining_track_len = 0 # to check that the track length specified is correct

        def advance(nibbles): 
            '''updates self.file_position and self.remaining_track_len
            'nibbles' is an integer representing the # of hex digits to advance
            Procedure (no return value)'''
            self.file_position += nibbles
            self.remaining_track_len -= nibbles

        # TODO improve this
        def print_bytes(data, explanation = " ", value = " ", offset = 0):
            '''pretty-prints a small chunk of byte(s) and an explanation of what they mean in the MIDI file
            'data' is a string of hex values representing the bytes to be explained
            'explanation' is an optional string describing what the data means
            'value' is an optional string for a variable value related to the meaning of the data
            'offset' is a switch:
                odd values mean the data starts halfway through a byte
                even values means the data starts at the beginning of a byte
                there is no need to set this value to anything besides 0 or 1
            Procedure (no return value)
            '''
            i = offset
            string = ""
            for c in data:
                string += str(c)
                if i % 2 == 1:
                    string += " "
                i += 1
            Logger.debug("\t", string, "=", explanation, value )

        # read header chunk:

        # check header chunk type
        if regex.match(r'4d546864', file_hex_str) == None:
            Logger.error("File does not begin with \"MThd\"")
        # self.file_position = 8
        advance(8)
        # check header length
        if regex.match(r'00000006', file_hex_str[self.file_position:self.file_position+8]) == None:
            Logger.error("Unrecognized header length: expected \"00000006\", but got: ", file_hex_str[self.file_position:self.file_position+8])
        # self.file_position += 8
        advance(8)
        # check format
        midi_format = int(file_hex_str[self.file_position:self.file_position+4], 16)
        if midi_format > 2:
            Logger.error("Unrecognized format: expected 0,1, or 2, but got: ", int(file_hex_str[self.file_position:self.file_position+4], 16))
        # self.file_position += 4
        advance(4)
        # get number of tracks
        num_tracks = int(file_hex_str[self.file_position:self.file_position+4], 16)
        # self.file_position += 4
        advance(4)
        print_bytes(file_hex_str[self.file_position:self.file_position+4], "Number of tracks: ", num_tracks)
        self.song_object.num_tracks = num_tracks
        # get division data 
        division = file_hex_str[self.file_position:self.file_position+4]
        print_bytes(file_hex_str[self.file_position:self.file_position+4], "Division: ", division)
        frmt = division[0:1]
        print_bytes(division[0:1], "Format: ", frmt)
        ticks_per_quarter_note = int(division[1:], 16)
        if int(frmt, 16) < 8:
            print_bytes(division[1:], "Ticks per quarter note: ", ticks_per_quarter_note, 1)
        # else:
            Logger.debug("Negative two's compliment of ", int(division[1:2], 16) - 128, "frames / second")
            Logger.debug(int(file_hex_str[self.file_position:self.file_position+2],16), "ticks / frame")
            self.song_object.timed = True
        # self.file_position += 4
        advance(4)
        self.song_object.ticks_per_quarter_note = ticks_per_quarter_note
        track_hex_str = file_hex_str
            
        Logger.debug("READ HEADER CHUNK OF SIZE ", self.file_position, "RESTARTING self.file_position at position ", self.file_position)
        # read track chunks
        for track_num in range(0, num_tracks):
            '''READS EACH TRACK CHUNK'''

            total_delta_time = 0
            # track_hex_str = track_hex_str[self.file_position:len(track_hex_str)]
            # check track chunk type
            print_bytes(track_hex_str[0:8], "\"MTrk\"")
            if track_hex_str[self.file_position:self.file_position+8] != "4d54726b":
                Logger.error("Track does not begin with \"MTrk\" ", "at position ", self.file_position)
            # if regex.match(r'4d54726b', track_hex_str) == None:
            #     Logger.error("Track does not begin with \"MTrk\" ", "at position ", self.file_position)
            # self.file_position += 8
            advance(8)
            # get track length
            track_len = int(track_hex_str[self.file_position : (self.file_position + 8)], 16)
            print_bytes(track_hex_str[self.file_position:self.file_position+8], "Track length: ", track_len)
            track_len *= 2 # measure in nibbles, not bytes
            self.remaining_track_len = track_len
            # self.file_position += 8
            advance(8)
            list_of_notes = []

            '''READS EACH DELTA_TIME - EVENT PAIR IN THE TRACK'''
            self.headless_event_counter = 0

            # self.previous_event_type = ""
            event_num = 0
            while self.remaining_track_len > -6: # 6 nibble end of track event not counted in length
                event_num += 1
                self.song_object.num_events
                '''READS EACH EVENT'''
                Logger.debug(f"█████Track {track_num} Event {event_num}█████")

                if self.remaining_track_len < 0:
                    Logger.error("Track length does not match up with length of track data")
                j = 0
                binary_value = ""
                while int(track_hex_str[self.file_position + j:self.file_position + j + 2], 16) >= 128:
                    binary_string = bin(int(track_hex_str[self.file_position + j: self.file_position + j + 2], 16))[2:].zfill(8)
                    binary_value += binary_string[1:8]
                    j += 2
                binary_string = bin(int(track_hex_str[self.file_position + j: self.file_position + j + 2], 16))[2:].zfill(8)
                binary_value += binary_string[1:8]
                delta_time = int(binary_value, 2)
                Logger.debug(f"\tDelta time: {delta_time} (0x{track_hex_str[self.file_position + j: self.file_position + j + 2]})")
                ''' 
                    From what I can tell, delta time is actually the amount of time (ticks) that pass before the next event (not since the last one). Therefore, to have correct note (and other event) start times, I have to add the delta time after creating the start time.
                '''
                start_ticks = total_delta_time
                total_delta_time += delta_time

                # TODO adjust time position
                advance(j+2)
                # if int(first_byte, 16) < 128:
                    # Logger.error("Unrecognized event at position ", self.file_position, ". Expected 0x80-0xFF, but got ", data[self.file_position:self.file_position+2])
                self.header_nibble_1 = track_hex_str[self.file_position] # first nibble of this event's data
                self.header_nibble_2 = track_hex_str[self.file_position+1] # second nibble of this event's data
                self.event_byte_2 = track_hex_str[self.file_position+2:self.file_position+4] # second byte of this event's data
                self.event_byte_3 = track_hex_str[self.file_position+4:self.file_position+6] # third byte of this event's data
                self.byte_4 = track_hex_str[self.file_position+6:self.file_position+8]
                Logger.debug(f"\tEvent starts at {hex(int(self.file_position/2))} header: {track_hex_str[self.file_position : self.file_position + 4]} data: {track_hex_str[self.file_position + 4 : self.file_position + 8]}")
                # self.previous_event_type = track_hex_str[self.file_position:self.file_position+6]

                def read_variable_length():
                    i = 0
                    binary_value = ""
                    while int(track_hex_str[self.file_position + i:self.file_position + i + 2], 16) >= 128:# reads one byte at a time; if first bit is 1, it continues
                        binary_string = bin(int(track_hex_str[self.file_position + i: self.file_position + i + 2], 16))[2:].zfill(8)
                        binary_value += binary_string[1:8]
                        i += 2
                    binary_string = bin(int(track_hex_str[self.file_position + i: self.file_position + i + 2], 16))[2:].zfill(8)
                    binary_value += binary_string[1:8]
                    length = int(binary_value, 2)
                    advance(i+2)
                    return length

                def get_text(nibbles = 2) -> str:
                    length = read_variable_length()
                    number_of_data_nibbles = length * 2
                    text_hex = track_hex_str[self.file_position:self.file_position + number_of_data_nibbles]
                    advance(number_of_data_nibbles)
                    text = bytearray.fromhex(text_hex).decode()
                    return text

                def read_midi_channel_prefix():
                    if track_hex_str[self.file_position:self.file_position+2] != '01':
                        Logger.error("Invalid MIDI Channel Prefix meta event found at position ", self.file_position, "(expected '11' but got ", track_hex_str[self.file_position:self.file_position+2],")")
                    elif int(track_hex_str[self.file_position+2:self.file_position+4], 16) > 15:
                        Logger.error("Invalid MIDI Channel Prefix meta event found at position ", self.file_position+2, "(expected 00-0f but got ", track_hex_str[self.file_position+2:self.file_position+4],")")
                    else:
                        set_channel(int(track_hex_str[self.file_position+2:self.file_position+4], 16) + 1)
                        advance(4)
                        return channel

                def read_midi_port():
                    if track_hex_str[self.file_position:self.file_position+2] != '01':
                        Logger.error("Invalid MIDI Port meta event found at position ", self.file_position, "(expected '01' but got ", track_hex_str[self.file_position:self.file_position+2],")")
                    else:
                        port = int(track_hex_str[self.file_position+2:self.file_position+4], 16) + 1
                        advance(4)
                        return port

                def hex_position(adjustment = 0):
                    file_position_in_decimal = int(self.file_position + adjustment)
                    if file_position_in_decimal % 2 == 0:
                        return hex(int(file_position_in_decimal/2))
                    else:
                        return hex(int(((file_position_in_decimal - 1) / 2) + 1))

                def parse_event(event_type):
                    Logger.debug(f"\tParsing event type: {event_names[event_type]} ({event_type})")

                    if event_type == Events.NOTE_ON:
                        # check/set key/velocity
                        key = int(track_hex_str[self.file_position:self.file_position+2], 16)
                        velocity = int(track_hex_str[self.file_position+2:self.file_position+4], 16)
                        # set channel
                        # if x == None:
                        set_channel(int(track_hex_str[self.file_position-1], 16) + 1)
                        # Logger.debug("\tEvent header:")
                        # print_bytes(track_hex_str[self.file_position-2:self.file_position+4], "Note on c nn vv")
                        Logger.debug(f"\tChannel nibble at 0x{track_hex_str[self.file_position - 1]} = {channel} ")
                        Logger.debug(f"\tKey byte {track_hex_str[self.file_position:self.file_position+2]} at {hex_position()} = {key}")
                        Logger.debug(f"\tVelocity byte {track_hex_str[self.file_position + 2 : self.file_position + 4]} at {hex_position(2)} = {velocity}")
                        # else:
                        # Logger.debug("Event header:")
                        # print_bytes(track_hex_str[self.file_position:self.file_position+4], "nn vv")
                        note_tuple = (key, channel, start_ticks)
                        found = False
                        if velocity == 0:
                            # if in list: create note object
                            for nt in list_of_notes: 
                                # create note object
                                if nt[0] == key and nt[1] == channel and not found:
                                    duration = total_delta_time - nt[2]
                                    note = self.song_object.add_note(start_ticks, duration, key, channel)
                                    Logger.debug("Note created: ", note.to_string(ticks_per_quarter_note))
                                    notes[channel].append(note)
                                    found = True
                                    Logger.debug("\tTurning off", key)
                                    list_of_notes.remove(nt) # remove from list_of_notes
                                    Logger.debug("\tNotes that are on: ", list_of_notes)
                            Logger.debug("found: ", found)
                            if not found:
                                Logger.debug("Note created with velocity of 0 at position")
                        else:
                            # add note to list
                            Logger.debug("\tTurning on", key)
                            list_of_notes.append(note_tuple)
                            Logger.debug("\tNotes that are on: ", list_of_notes)
                        advance(4)# add note event is 3 bytes long
                        Logger.debug("\tNotes that are on:", list_of_notes)
                    elif event_type == Events.NOTE_OFF:
                        Logger.debug("\tNote off event")
                        # check/set key/velocity
                        key = int(track_hex_str[self.file_position:self.file_position+2], 16)
                        velocity = int(track_hex_str[self.file_position+2:self.file_position+4], 16)
                        Logger.debug("\tTurning off", key)
                        # set channel
                        # if x == None:
                        set_channel(int(track_hex_str[self.file_position-1], 16) + 1)
                        print_bytes(track_hex_str[self.file_position-2:self.file_position+4], "Note off c nn vv")
                        # else:
                        print_bytes(track_hex_str[self.file_position:self.file_position+4], "nn vv")
                        Logger.debug("\tChannel: ", channel)
                        # if in list: create note object
                        found = False
                        Logger.debug("\tNotes that are on: ", list_of_notes)
                        for nt in list_of_notes: 
                            # create note object
                            Logger.debug(nt[0], "=? ", key, " ", nt[1], "=? ", channel)
                            if nt[0] == key and nt[1] == channel and not found:
                                duration = total_delta_time - nt[2]
                                start = start_ticks
                                note = self.song_object.add_note(start_ticks, duration, key, channel)
                                Logger.debug("Note created: ", note.to_string(ticks_per_quarter_note))
                                notes[channel].append(note)
                                found = True
                                list_of_notes.remove(nt) # remove from list_of_notes
                                Logger.debug("\tNotes that are on: ", list_of_notes)
                            Logger.debug("found: ", found)
                        if not found:
                            Logger.error(f"Invalid note off event at position {self.file_position} ({hex(int(self.file_position/2))}). No such note of pitch {key} is currently on")
                        Logger.debug("Add/Pop Note Command at position: ", self.file_position)
                        advance(4) # add note event is 3 bytes long
                        Logger.debug("\tNotes that are on: ", list_of_notes)
                    elif event_type == Events.POLYPHONIC:
                        # check/set key/velocity
                        # set channel
                        # send message
                        Logger.debug("Polyphonic Note at position: ", self.file_position)
                        Logger.warn("Polyphonic notes not yet delt with in this project")
                        advance(4) # polyphonic note event has 4 nibbles after the header
                    elif event_type == Events.PROGRAM_CHANGE:
                        # check new_program_# 
                        # send message
                        Logger.warn(f"Program Change at position {self.file_position} ({hex(int(self.file_position/2))}). This project currently does nothing with these")
                        print_bytes(track_hex_str[self.file_position-2:self.file_position+2], "Program change to ", int(track_hex_str[self.file_position:self.file_position+2], 16))
                        advance(2)
                    elif event_type == Events.PRESSURE_CHANGE:
                        # check channel_pressure_val
                        # send message
                        Logger.debug("Channel Key Pressure of ", track_hex_str[self.file_position:self.file_position+2], "at position: ", self.file_position)
                        advance(2)# channel key pressure event is 2 bytes long
                    elif event_type == Events.PITCH_CHANGE:
                        # check msb, lsb
                        # send message
                        Logger.debug("Pitch Bend at position: ", self.file_position)
                        advance(4)# pitch bend event is 3 bytes long
                    elif event_type == Events.ARBITRARY_TEXT:
                        Logger.debug("Arbitrary text meta event read at position ", self.file_position)
                        advance(4)
                        text = get_text().decode("hex")
                        Logger.debug("Text: ", text)
                    elif event_type == Events.TRACK_NAME:
                        # Sequence/Track Name
                        # read_sequence_track_name()
                        Logger.debug("Sequence/Track Name meta event read at position ", self.file_position)
                        advance(4)
                        seq_track_name = get_text().decode("hex")
                        Logger.debug("Sequence/Track Name: ", seq_track_name)
                    elif event_type == Events.INSTRUMENT_NAME:
                        # Instrument Name
                        Logger.debug("Instrument Name meta event read at position ", self.file_position)
                        advance(4)
                        instrument_name = get_text().decode("hex")
                        Logger.debug("Instrument Name: ", instrument_name)
                    elif event_type == Events.PROGRAM_NAME:
                        Logger.debug(f"Program Name meta event read at position {self.file_position}")
                        program_name = get_text()
                        self.song_object.title = program_name
                        Logger.debug(f"Program Name: \'{program_name}\'")
                    elif event_type == Events.COMPOSER_NAME:
                        # THIS IS NOT ON THE INTERNET FOR SOME REASON BUT IT'S A FREAKING THING AND I HAD TO FIGURE IT OUT FOR MYSELF
                        Logger.debug(f"Composer Name meta event read at position self.file_position")
                        composer_name = get_text()
                        Logger.debug(f"Composer Name: \'{composer_name}\'")
                    elif event_type == Events.TIME_SIGNATURE:
                        Logger.debug(f"Time signature event at {self.file_position} ({hex(int(self.file_position/2))})")
                        if track_hex_str[self.file_position:self.file_position+2] != "04":
                            Logger.error("Unrecognized Time Signature meta event at position ", self.file_position, "found ", track_hex_str[self.file_position+4:self.file_position+6], "but expected 0x04")
                        else:
                            numerator = int(track_hex_str[self.file_position+2:self.file_position+4], 16)
                            denominator = 2 ** int(track_hex_str[self.file_position+4:self.file_position+6], 16)
                            cc = int(track_hex_str[self.file_position+6:self.file_position+8], 16) # number of MIDI clocks in a metronome click
                            bb = int(track_hex_str[self.file_position+8:self.file_position+10], 16) # number of notated 32nd notes in a MIDI quarter note (24 MIDI clocks)
                            time_signature = str(numerator) + "/" + str(denominator)
                            self.song_object.time_signature = time_signature
                            Logger.debug("Time signature: ", numerator, "/", denominator)
                        advance(10)
                    elif event_type == Events.KEY_SIGNATURE:
                        if track_hex_str[self.file_position:self.file_position+2] != "02":
                            Logger.error("Unrecognized Key Signature meta event at position ", self.file_position, "found ", track_hex_str[self.file_position+4:self.file_position+6], "but expected 0x02")
                        else:
                            numsharps = int(track_hex_str[self.file_position+2:self.file_position+4], 16)
                            mode = track_hex_str[self.file_position+4:self.file_position+6]
                            majorkeys = {	249 : "C flat major ",
                                            250 : "G flat major ",
                                            251 : "D flat major ",
                                            252 : "A flat major ",
                                            253 : "E flat major ",
                                            254 : "B flat major ",
                                            255 : "F major ",
                                            0  : "C major ",
                                            1  : "G major ",
                                            2  : "D major ",
                                            3  : "A major ",
                                            4  : "E major ",
                                            5  : "B major ",
                                            6  : "F sharp major ",
                                            7  : "C sharp major"}
                            minorkeys = {	5  : "C flat minor ",
                                            6  : "G flat minor ",
                                            7  : "D flat minor ",
                                            249 : "A flat minor ",
                                            250 : "E flat minor ",
                                            251 : "B flat minor ",
                                            252 : "F minor ",
                                            253 : "C minor ",
                                            254 : "G minor ",
                                            255 : "D minor ",
                                            0  : "A minor ",
                                            1  : "E minor ",
                                            2  : "B minor ",
                                            3  : "F sharp minor ",
                                            4  : "C sharp minor"}
                            if mode == b"00":
                                self.song_object.key = majorkeys[numsharps]
                                Logger.debug("Key signature: ", majorkeys[numsharps])
                            else:
                                self.song_object.key = minorkeys[numsharps]
                                Logger.debug("Key signature: ", minorkeys[numsharps])
                        advance(6)
                    elif event_type == Events.END_OF_TRACK:
                        if track_hex_str[self.file_position:self.file_position+2] == '00':
                            Logger.debug("********************YAAAAAAY********************")
                            advance(2)
                        else:
                            Logger.error("Unrecognized End of Track meta event found at position ", self.file_position, "found ", track_hex_str[self.file_position:self.file_position+2], "but expected 0x00")
                    elif event_type == Events.SEQUENCE_SPECIFIER:
                        # TODO this could be a variable # of bytes
                        # Sequencer-Specific
                        Logger.error("Sequence-Specific meta event read at position ", self.file_position)
                        # read_sequence_specific()
                        advance(4)
                        program_name = get_text().decode("hex")
                        Logger.debug("Sequence-Specific: ", program_name)
                    elif event_type == Events.SET_TEMPO:
                        if track_hex_str[self.file_position:self.file_position+2] != "03":
                            Logger.error("Unrecognized Set Tempo meta event at position ", self.file_position, "found ", track_hex_str[self.file_position:self.file_position+2], "but expected 0x03")
                        else:
                            microsec_per_quarter_note = int(track_hex_str[self.file_position+2:self.file_position+8], 16)
                        Logger.debug(f"Tempo set to {microsec_per_quarter_note} microseconds per quarter note ({round(60000000/microsec_per_quarter_note)} beats per minute)")
                        advance(8)
                    elif event_type == Events.CONTROL_CHANGE:
                        # check control# , control_val
                        # send message
                        Logger.warn("\tControl changes are usually not in MIDI scores. These events are currently unread in this project")
                        print_bytes(track_hex_str[self.file_position:self.file_position+4], "Control change")
                        advance(2) # control change event is 1 byte after the header
                    elif event_type == Events.NOT_YET_DEALT_WITH:
                        Logger.error(f"Encountered a header that is not yet dealt with in this program at position {self.file_position-4}")
                    else:
                        Logger.error(f"Event type set to {event_type}")

                def determine_event(event_header) -> str:
                    # advance(4) # All headers should be 4 nibbles long
                    event_type = ""
                    # Logger.debug(f"Header nibble 1: {event_header[0]}, Header nibble 2: {event_header[1]}, Header byte 2: {event_header[2:4]}")
                    '''HANDLE MIDI EVENTS'''
                    if event_header[0] == '8':
                        advance(2)
                        event_type = Events.NOTE_OFF
                    elif event_header[0] == '9':
                        advance(2)
                        event_type = Events.NOTE_ON
                    elif event_header[0] == 'a':
                        advance(2)
                        event_type == Events.POLYPHONIC
                    elif event_header[0] == 'b':
                        advance(2)
                        event_type = Events.CONTROL_CHANGE
                    elif event_header[0] == 'c':
                        advance(2)
                        event_type = Events.PROGRAM_CHANGE
                    elif event_header[0] == 'd':
                        advance(2)
                        event_type = Events.PRESSURE_CHANGE
                    elif event_header[0] == 'e':
                        advance(2)
                        event_type = Events.PITCH_CHANGE
                    elif event_header[0] == 'f':
                        '''HANDLE SYSEX EVENTS'''
                        if event_header[1] == 0:
                            event_type = Events.NOT_YET_DEALT_WITH
                        elif event_header[1] == 7:
                            event_type = Events.NOT_YET_DEALT_WITH
                        elif event_header[1] == 'f':
                            '''HANDLE META EVENTS'''
                            if event_header[2:4] == '00':
                                event_type = Events.NOT_YET_DEALT_WITH
                            elif event_header[2:4] == '01':
                                advance(4)
                                event_type = Events.ARBITRARY_TEXT
                            elif event_header[2:4] == '02':
                                event_type = Events.NOT_YET_DEALT_WITH
                            elif event_header[2:4] == '03':
                                advance(4)
                                event_type = Events.TRACK_NAME
                            elif event_header[2:4] == '04':
                                advance(4)
                                event_type = Events.INSTRUMENT_NAME
                            elif event_header[2:4] == '05':
                                event_type = Events.NOT_YET_DEALT_WITH
                            elif event_header[2:4] == '06':
                                event_type = Events.NOT_YET_DEALT_WITH
                            elif event_header[2:4] == '07':
                                event_type = Events.NOT_YET_DEALT_WITH
                            elif event_header[2:4] == '08':
                                advance(4)
                                event_type = Events.PROGRAM_NAME
                            elif event_header[2:4] == '0a':
                                advance(4)
                                event_type = Events.COMPOSER_NAME
                            elif event_header[2:4] == '2f':
                                advance(4)
                                event_type = Events.END_OF_TRACK
                            elif event_header[2:4] == '51':
                                advance(4)
                                event_type = Events.SET_TEMPO
                            elif event_header[2:4] == '54':
                                event_type = Events.NOT_YET_DEALT_WITH
                            elif event_header[2:4] == '58':
                                advance(4)
                                event_type = Events.TIME_SIGNATURE
                            elif event_header[2:4] == '59':
                                advance(4)
                                event_type = Events.KEY_SIGNATURE
                            elif event_header[2:4] == '7f':
                                advance(4)
                                event_type = Events.SEQUENCE_SPECIFIER
                    if event_type == "": # no event_type found
                        if event_header[0] in ['8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
                            Logger.error(f"\tEvent header {event_header} is not recognized. If this is not an event header, it should not start with an on bit (1)")
                        Logger.debug(f"\t{event_names[self.previous_event_type]} with no header at {self.file_position} ({hex(int(self.file_position/2))})")
                        self.headless_event_counter += 1
                        Logger.debug(f"\tThis is headless event #{self.headless_event_counter}")
                        parse_event(self.previous_event_type)
                    else:
                        self.previous_event_type = event_type
                        Logger.debug(f"\t{event_names[event_type]} event header starts at {self.file_position} ({hex(int(self.file_position/2))})")
                        # advance(4)
                        self.headless_event_counter = 0
                        parse_event(event_type)
                event_header = track_hex_str[self.file_position:self.file_position+6]
                determine_event(event_header)
        
            if track_hex_str[-6:] != 'ff2f00':
                Logger.error(f"Last 3 bytes {track_hex_str[-6:]} should have been ff2f00")
                Logger.error("Track does not end with end_of_track meta event")
      
        
        
        
        Logger.debug(f"{self.file_path} is a valid MIDI file.")
        number_of_notes = 0
        note_list = []
        for c in notes:
            for n in notes[c]:
                note_list.append(n)
                number_of_notes += 1
                # Logger.debug(n.to_string(ticks_per_quarter_note))
        Logger.debug("Number of notes in file: ", number_of_notes)
        self.song_object.notes = notes
        self.song_object.num_channels = len(channels)
        return self.song_object

