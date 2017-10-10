from osgeo import gdal
gdal.UseExceptions()

fn = '/u/cliffk/cliff/music/london2017/elevation/n41_e048_1arc_v3.tif'
fn2 = '/u/cliffk/cliff/music/london2017/elevation/n41_e047_1arc_v3.tif'

ds = gdal.Open(fn2)
band = ds.GetRasterBand(1)
elevation = band.ReadAsArray()

print elevation.shape
print elevation

plt.figure(facecolor='w')
import matplotlib.pyplot as plt
plt.imshow(elevation, cmap='gist_earth')
plt.show()

vector = []
for i in range(elevation.shape[0]):
    vector.append(elevation[i,i])

plt.figure(facecolor='w')
plt.plot(vector)