f = open("a.mid", "rb")
try:
    byte = f.read(1)
    while byte != "":
        print byte
        byte = f.read(1)
finally:
    f.close()