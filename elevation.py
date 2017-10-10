#%%
print('Importing libraries...')
from osgeo import gdal
from pylab import array, zeros, figure, imshow, nan

#%%
print('Defining parameters...')
folder = '/u/cliffk/cliff/music/london2017/elevationdata/'
controlstr = 'n%02i_e%03i_1arc_v3.tif'
North = [41, 42, 43]
East = range(39,49)

#%%
print('Loading files...')
data = []
ncoords = []
ecoords = []
nfiles = 0
for north in North:
    for east in East:
        string = controlstr % (north, east)
        fn = folder+string
        print('Loading %s...' % fn)
        try:
            ds = gdal.Open(fn)
            elevation = ds.GetRasterBand(1).ReadAsArray()
            data.append(elevation)
            ncoords.append(north)
            ecoords.append(east)
            nfiles += 1
        except Exception as E:
            pass # print('No matter: %s' % E.__repr__())

#%%
print('Processing...')
npts = elevation.shape[0]
ncoords = array(ncoords)
ecoords = array(ecoords)
ncoords -= ncoords.min()
ecoords -= ecoords.min()
northpts = npts*(ncoords.max()+1)
eastpts  = npts*(ecoords.max()+1)
fulldata = zeros((northpts,eastpts))+nan
for f in range(nfiles):
    npos = (ncoords.max()-ncoords[f])*npts
    epos = ecoords[f]*npts
    thisdata = data[f]
    fulldata[npos:npos+npts, epos:epos+npts] = thisdata

#%%
print('Subsampling...')
subsamp = int(eastpts/1980)
subdata = fulldata[::subsamp,::subsamp]

#%%
print('Plotting...')
figure(facecolor='w')
imshow(subdata, cmap='gist_earth')

#vector = []
#for i in range(elevation.shape[0]):
#    vector.append(elevation[i,i])
#plt.figure(facecolor='w')
#plt.plot(vector)