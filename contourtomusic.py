"""
Version:
"""

from pylab import loadtxt, plot, interp, arange, linspace

trimstart = 200
trimend = 400
fn = 'rawcontour.txt'
octaves = 4
seconds = 180
notesperoctave = 12
notespersecond = 4

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

