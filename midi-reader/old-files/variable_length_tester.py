
fp=0
def advance(nibbles): 
    '''updates fp and remaining_track_len
    'nibbles' is an integer representing the # of hex digits to advance
    Procedure (no return value)'''
    global fp
    fp += nibbles

#TODO this isn't used??? how is it not used at all?
def read_variable_length():
    i = 0
    binary_value = ""
    while int(data[fp + i], 16) >= 8:#reads one byte at a time; if first bit is 1, it continues
        binary_string = bin(int(data[fp + i: fp + i + 2], 16))[2:].zfill(8)
        binary_value += binary_string[1:8]
        i += 2
    binary_string = bin(int(data[fp + i: fp + i + 2], 16))[2:].zfill(8)
    binary_value += binary_string[1:8]
    length = int(binary_value, 2)
    advance(i+2)
    return length
data = "7f817f828000"
print "Hex: 7F should return 127, but returns: ", read_variable_length()
print "Hex: 81 7F should return 255, but returns: ", read_variable_length()
print "Hex: 82 80 00 should return 32768, but returns: ", read_variable_length()
