"""
Version:
"""

from pylab import loadtxt, plot, interp, arange, linspace
from playpiece import note


# Parameters
trimstart = 200
trimend = 400
fn = 'rawcontour.txt'
octaves = 4
seconds = 180
notesperoctave = 12
notespersecond = 4

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
plot(contour)

# Convert to notes
pitches = []
for val in contour:
    pitches.append(makepitch(val))

# Play
duration = 10.0/notespersecond
for pitch in pitches:
    print pitch
#    note(frequency=pitch, duration=duration)