from math import modf as get_fraction_and_integer_parts

from Tools.Logger import Logger


class Note:
    def __init__(self):
        self.pitch = 0
        self.start = 0
        self.duration = 0
        self.channel = 0

    def __init__(self, start, duration, pitch, channel, ticks_per_quarter_note = None):
        def round_rhythm(time):
            frac, whole = get_fraction_and_integer_parts(time)
            Logger.debug("\tTime:", time, "Fraction:", frac, "Whole:", whole)
            if  frac < .1:
                frac = 0.0
                Logger.debug("\tfrac < .1 so frac is being rounded to 0.0")
            elif frac > .9:
                whole += 1
                frac = 0.0
                Logger.debug("\tfrac > .9 so frac is being rounded to 0.0 and 1 is being added to whole")
            elif frac > .2 and frac < .28:
                frac = 0.25
                # Logger.debug("\nfrac > .2 -> frac := 0.25")
            elif frac > .29 and frac < .4:
                frac = 1.0/3.0
                # Logger.debug("\nfrac > .29 -> frac := ")
            elif frac > .45 and frac < .55:
                frac = 0.5
                # Logger.debug("\nfrac > .2 -> frac := 0.25")
            elif frac > .56 and frac < .7:
                frac = 2.0/3.0
                # Logger.debug("\nfrac > .2 -> frac := 0.25")
            elif frac > .7 and frac < .8:
                frac = 0.75
                # Logger.debug("\nfrac > .2 -> frac := 0.25")
            else:
                Logger.debug("!!!!!!!!!!")
            Logger.debug("\tRounded rhythm: ", whole, " + ", frac, " = ", whole+frac)
            return whole+frac
        self.pitch = pitch
        self.channel = channel
        if ticks_per_quarter_note == None:
            self.start = start*960
            self.duration = duration*960
        else:
            # Logger.debug("\t+++", start % 480, "ticks -> ", (round_rhythm(start / float(ticks_per_quarter_note))), "beats")
            # Logger.debug("\t+++", duration, "ticks -> ", (round_rhythm(duration / float(ticks_per_quarter_note))), "beats")
            self.start = round_rhythm(start / float(ticks_per_quarter_note))
            # Logger.debug("{{{", duration, ticks_per_quarter_note, duration / float(ticks_per_quarter_note))
            Logger.debug("\tStart ticks: ", start, " / ", ticks_per_quarter_note, "ticks/qtr-note = ", self.start, "qtr-notes")
            self.duration = round_rhythm(duration / float(ticks_per_quarter_note))
            Logger.debug("\tDuration ticks: ", duration, " / ", ticks_per_quarter_note, "ticks/qtr-note = ", self.duration, "qtr-notes")
            

    #TODO instead of converting ticks to rhythm here, do it in the midi_reader file
    def to_string(self, ticks_per_quarter_note = None):
            #TODO make sharps an option
            notes = {	0 : 'C',
                        1 : 'Db',
                        2 : 'D',
                        3 : 'Eb',
                        4 : 'E',
                        5 : 'F',
                        6 : 'Gb',
                        7 : 'G',
                        8 : 'Ab',
                        9 : 'A',
                        10: 'Bb',
                        11: 'B',
                        }
            string = ""
            note = str(notes[self.pitch % 12]) + str(self.pitch // 12 + 1)
            # if ticks_per_quarter_note == None:
            # 	string = "Channel: "
            # 	string += self.channel, "Pitch:", self.pitch, "start:", self.start*960, "seconds", "Duration:", self.duration*960, "seconds"
            # else:
            # 	string = "Channel: "
            # 	string += str(self.channel) + ", Pitch: " + note + ", start: " + str(round_rhythm(self.start / float(ticks_per_quarter_note))) + " quarter notes, Duration: " + str(round_rhythm(self.duration / float(ticks_per_quarter_note))) + " quarter notes"
            
            if ticks_per_quarter_note == None:
                string = "Channel: "
                string += self.channel, " Pitch: ", self.pitch, " start: ", self.start*960, " seconds ", " Duration: ", self.duration*960, " seconds"
            else:
                string = "Channel: "
                string += str(self.channel) + ", Pitch: " + note + ", start: " + str(round(self.start, 2)) + " quarter notes, Duration: " + str(round(self.duration, 2)) + " quarter notes"
            return string
            
    def overlap(self, note):
        a = self.start
        b = self.start + self.duration
        x = note.start
        y = note.start + note.duration

        if x >= b or a >=y:
            return 0
        elif a <= x and b <= y:
            return 2 * (b-x) / (self.duration + note.duration)
        elif a <= x and b >= y:
            return 2 * (note.duration) / (self.duration + note.duration)
        elif a >= x and b <= y:
            return 2 * (y-a) / (self.duration + note.duration)
        elif a >= x and b >= y:
            return 2 * (self.duration) / (self.duration + note.duration)
