class Events:
    # Channel Voice Messages
    NOTE_OFF = '8xxx'
    NOTE_ON = '9xxx'
    POLYPHONIC = 'axxx'

    # MIDI Channel Voice Changes
    '''All channel voice changes specify the channel in the second header nibble'''
    CONTROL_CHANGE = 'bxxx'
    PROGRAM_CHANGE = 'cxxx'
    PRESSURE_CHANGE = 'dxxx'
    PITCH_CHANGE = 'exxx'
    
    # SYSEX Events
    SYSEX = 'f0xx'

    # Meta Events
    SEQUENCE_NUMBER = 'ff00'
    ARBITRARY_TEXT = 'ff01'
    COPYRIGHT_NOTICE = 'ff02'
    TRACK_NAME = 'ff03'
    INSTRUMENT_NAME = 'ff04'
    LYRIC = 'ff05'
    MARKER = 'ff06'
    CUE_POINT = 'ff07'
    PROGRAM_NAME = 'ff08'
    COMPOSER_NAME = 'ff0a'
    END_OF_TRACK = 'ff2f'
    SET_TEMPO = 'ff51'
    SMTPE_OFFSET = 'ff54'
    TIME_SIGNATURE = 'ff58'
    KEY_SIGNATURE = 'ff59'
    SEQUENCE_SPECIFIER = 'ff7f'

    # Misc
    NOT_YET_DEALT_WITH = 'xxxx'

event_names = {
    '8xxx': "Note Off",
	'9xxx': "Note On",
	'axxx': "Polyphonic",
	'bxxx': "Control Change",
	'cxxx': "Program Change",
	'dxxx': "Pressure Change",
	'exxx': "Pitch Change",
	'f0xx': "Sysex",
	'ff00': "Squence Number",
	'ff01': "Text",
	'ff02': "Copyright Notice",
	'ff03': "Track Name",
	'ff04': "Instrument Name",
	'ff05': "Lyric",
	'ff06': "Marker",
	'ff07': "Cue Point",
	'ff08': "Program Name",
	'ff0a': "Composer Name",
	'ff2f': "End of Track",
	'ff51': "Set Tempo",
	'ff54': "SMTPE Offset",
	'ff58': "Time Signature",
	'ff59': "Key Signature",
	'ff7f': "Sequence Specifier",
	'xxxx': "Unknown"
}