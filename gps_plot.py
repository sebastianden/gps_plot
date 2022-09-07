# %%
import tilemapbase
import matplotlib.pyplot as plt
import gpxpy
import glob
import numpy as np

# %%
lat, lon = [], []

for file in glob.glob('*.gpx'):
    gpx_file = open(file, 'r')
    gpx = gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)

lat = np.array(lat)
lon = np.array(lon)
path = [tilemapbase.project(x, y) for x, y in zip(lon, lat)]
x, y = zip(*path)


# %%
tilemapbase.init(create=True)
t = tilemapbase.tiles.build_OSM()
extent = tilemapbase.Extent.from_lonlat(-19.8, -18.8,
                                        63.6, 64.1)
#extent = extent.to_aspect(1.0)
fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
plotter = tilemapbase.Plotter(extent, t, width=500)
plotter.plot(ax, t)

ax.plot(x, y, '--r')
plt.show()
# %%
