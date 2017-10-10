"""
Version:
"""

from pylab import loadtxt, plot, interp, arange, linspace
from playpiece import makenote, play
from midiutil.MidiFile import MIDIFile

# Parameters
trimstart = 200
trimend = 400
fn = 'rawcontour.txt'
midifn = 'contours.mid'
octaves = 4
seconds = 180
notesperoctave = 12
notespersecond = 4
converttonotes = False
converttomidi = True

duration = 1#1.0/notespersecond

def makepitch(val, fundamental=100):
    ''' Turn a number of semitones into a pitch '''
    semitone = 2**(1/12.)
    pitch = fundamental*semitone**val
    return pitch

rawcontour = loadtxt(fn)
contour = rawcontour[::-1][trimstart:-trimend] # Reverse order

# Process length
numnotes = seconds*notespersecond
origx = arange(len(contour))
newx = linspace(origx[0], origx[-1], numnotes)
contour = interp(newx, origx, contour) 

# Process pitch
maxnotes = octaves*notesperoctave
contour -= contour.min()
contour *= maxnotes/float(contour.max())
contour = contour.round()
#plot(contour)

#%%
if converttonotes:
    # Convert to notes
    pitches = []
    for val in contour:
        pitches.append(makepitch(val))
    # Play
    
    notes = []
    for pitch in pitches:
        print pitch
        thisnote = makenote(frequency=pitch, duration=duration)
        notes += thisnote
    play(notes)
    
    
#%%
if converttomidi:
    offset = 30 # To start from the correct note
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats
    tempo    = 300   # In BPM
    volume   = 100  # 0-127, as per the MIDI standard
    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    MyMIDI.addTempo(track, time, tempo)
    for i, pitch in enumerate(contour):
        print pitch
        MyMIDI.addNote(track, channel, pitch+offset, time + i, duration, volume)
    
    with open(midifn, "wb") as output_file:
        MyMIDI.writeFile(output_file)
        