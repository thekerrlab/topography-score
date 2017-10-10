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
    mf = MIDIFile(1)     # create your MIDI object
    track = 0   # the only track
    time = 0    # start at the beginning
    channel = 0
    volume = 100
    time = 0             # start on beat 0
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 60)
    for pitch in contour: # add some notes
        mf.addNote(track, channel, pitch, time, duration, volume)
    with open(midifn, 'wb') as outf: mf.writeFile(outf) # write it to disk
        