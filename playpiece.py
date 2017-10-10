"""
From https://stackoverflow.com/questions/26761055/synthesizing-an-audio-pitch-in-python
"""


import pyaudio
import struct
import math

SHRT_MAX=32767 # short uses 16 bits in complement 2
sample_width=2  
sample_rate = 44100

def my_sin(t,frequency):
    radians = t * frequency * 2.0 * math.pi
    pulse = math.sin(radians)
    return pulse

#pulse_function creates numbers in [-1,1] interval
def makenote(frequency=1000, duration=1, amplitude=1):
    sample_duration = 1.0/sample_rate
    total_samples = int(sample_rate * duration)
    note = []
    for n in range(total_samples):
        t = n*sample_duration
        tmp = int(SHRT_MAX*my_sin(t, frequency))
        note.append(tmp)
    return note

def play(data):
    p = pyaudio.PyAudio()
    pformat = p.get_format_from_width(sample_width)
    stream = p.open(format=pformat,channels=1,rate=sample_rate,output=True)
    for d in data:
        streamdata = struct.pack("h",d)
        stream.write(streamdata)


#example of a function I took from wikipedia.
major_chord = f = lambda t: (my_sin(t,440)+my_sin(t,550)+my_sin(t,660))/3

#choose any frequency you want
#choose amplitude from 0 to 1
#def playnote(frequency=1000, amplitude=1, duration=1, doplay=True):
#    f = lambda t: amplitude * my_sin(t,frequency)
#    if doplay:
#        play()
#    else:
#        return f

#if __name__=="__main__":
#    # play fundamental sound at 1000Hz for 5 seconds at maximum intensity
#    playnote(1000,1)
#    note(500,1)
#    note(500,0.5)





#import audiogen
#
#beats = audiogen.mixer(
#        (audiogen.tone(440), audiogen.tone(445)),
#        [(1, 1)]
#)
#
#audiogen.sampler.play(beats)