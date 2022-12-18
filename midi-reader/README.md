# MIDI File Format

MIDI stands for Musical Instrument Digital Interface. It was defined in 1983 and is still partially used by music notation software.

MIDI files are created as streams of binary data.

MIDI files consist of several chunks
* A header chunk
* 1 or more track chuncks

## Header Chunk

1) The header chunk starts with the data "MThd" as 4 bytes of data. In hex that is 4d 54 68 64.
2) 4 bytes that define the length of the remainder of the header chunk (the value is always 6)
3) 2 bytes that define the format of the file
    - 0 = single track file format
    - 1 = multiple track file format
    - 2 = multiple song file format
4) 2 bytes that define the number of tracks in the file
5) 2 bytes that define the timing of the file
    - Positive numbers represent ticks per beat
    - Negative numbers represent SMPTE units

Example:
4d 54 68 64 00 00 00 06 00 01 00 04 01 e0

| Raw (Hex)   | Value  | Description            |
| ----------- | -------| ---------------------- |
| 4d 54 68 64 | "MThd" | Header chunk signature |
| 00 00 00 06 | 0006   | Remaining length of header |
| 00 01       | 1      | Multi-track file |
| 00 04       | 4      | 4 tracks in this file |
| 01 e0       | 480    | 480 ticks per beat |

## Track Chunk

1) Each track chunk starts with the signature "MTrk" as the firs 4 btyes of data (4d 54 72 6b in hex)
2) 4 bytes that specify the remaining length of this chunk
3) 1 or more track events

Example:
4d 54 72 6b 00 00 07 63 

| Raw (Hex)   | Value  | Description            |
| ----------- | -------| ---------------------- |
| 4d 54 72 6b | "MTrk" | Track chunk signature |
| 00 00 07 63 | 1,891  | Remaining length of track |
| 00 ff 08 ...| ...    | Track events... |

### Track Events

1) Every event starts with a [variable length](#Variable-length) that specifies the time passed before this event
2) Event header of 1 nibble to 2 bytes in length*
(The event header can be skipped which implies that the next event is of the same type as the previous)
3) 1 or more data bytes

* Each track event can be 1 or 3 types
1) MIDI event which contain information about the audio in the file
2) Meta events which give information about the file
3) SysEx (system exclusive) SMF (standard MIDI file) events

Example:
00 ff 08 14 41 69 72 20 6f 6e 20 74 68 65 20 47 20 53 74 72 69 6e 67 00 

| Raw (Hex)   | Value  | Description            |
| ----------- | -------| ---------------------- |
| 00          | 0      | Delta time of 0 ticks  |
| ff 08       | NA     | Event header defining a program name event |
| 14          | 20     | Remaining length of event data = 20 bytes |
| 41 69 72 20 6f 6e 20 74 68 65 20 47 20 53 74 72 69 6e 67 00 | "Air on the G String" | Name of the file |

### Variable length

1 or more bytes used to specify delta time values or the remaining length of an event
* Only the last 7 bits of each bytes is used to 
* The final byte of variable length begins with a 0 bit
    * 01111111 (127) is the largest length representable by a single-byte variable length
* If extra bytes are needed to define a length of longer than 127, those bytes preceed the final byte and start with a 1 bit
    * This is rare

### MIDI Events

1) Start with a 1 bit, so the first nibble value is 8-f
2) 1 nibble defining the channel that this event occurs on
3) 1 or 2 bytes of data

Example:
delta_time + event_header + channel + data = 00 + 9 + 3f + 40

**MIDI Event Types**

| Type            | Header Nibble | Data                       | Values                                                          |
| --------------- | ------------- | -------------------------- | --------------------------------------------------------------- |
| Note Off        | 8             | nnnn, 0kkk kkkk, 0vvv vvvv | nnnn: channel (0-15), kkkkkkk: note key, vvvvvvv: note velocity |
| Note On         | 9             | nnnn, 0kkk kkkk, 0vvv vvvv | nnnn: channel (0-15), kkkkkkk: note key, vvvvvvv: note velocity |
| Polyphonic Note | a             | nnnn, 0kkk kkkk, 0vvv vvvv | nnnn: channel (0-15), kkkkkkk: note key, vvvvvvv: note velocity |
| Control Change* | b             | nnnn, 0ccc cccc, 0vvv vvvv | nnnn: channel (0-15), ccccccc: controller number, vvvvvvv: new value |
| Program Change  | c             | nnnn, 0ppp pppp | nnnn: channel (0-15), ppppppp: new program number |
| Pressure Change | d             | nnnn, 0vvv vvvv | nnnn: channel (0-15), vvvvvvv: max pressure value |
| Pitch Change    | e             | nnnn, 0lll llll, 0mmm mmmm | nnnn: channel (0-15), lllllll: least significant 7 bits, mmmmmmm: most significant 7 bits |
| NA              | f             | NA | NA |

*Control change events could also be channel mode messages which add more complications

**Meta Event Types**
