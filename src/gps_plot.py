import glob
from typing import Tuple
import gpxpy
import matplotlib.pyplot as plt
import tilemapbase


def load_gps_data() -> Tuple[list, list]:
    """_summary_

    Returns:
        Tuple[list, list]: _description_
    """
    lon, lat = [], []

    for file in glob.glob('*.gpx'):
        gpx_file = open(file, 'r')
        gpx = gpxpy.parse(gpx_file)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lon.append(point.longitude)
                    lat.append(point.latitude)

    return lon, lat


def create_map(lon: list, lat: list) -> None:
    """_summary_

    Args:
        lon (list): _description_
        lat (list): _description_
    """
    f = 0.25
    path = [tilemapbase.project(x, y) for x, y in zip(lon, lat)]
    edges = (min(lon), max(lon), min(lat), max(lat))
    lon_range, lat_range = edges[1] - edges[0], edges[3] - edges[2]
    edges = (
        edges[0] - f * lon_range, edges[1] + f * lon_range,
        edges[2] - f * lat_range, edges[3] + f * lat_range
    )
    x, y = zip(*path)

    tilemapbase.init(create=True)
    t = tilemapbase.tiles.build_OSM()
    extent = tilemapbase.Extent.from_lonlat(*edges)
    extent = extent.to_aspect(1.0, False)
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    plotter = tilemapbase.Plotter(extent, t, width=500)
    plotter.plot(ax, t)
    ax.plot(x, y, color='brown', linestyle='dashed')
    plt.savefig('test.jpg', dpi=300)


if __name__ == "__main__":

    x, y = load_gps_data()

    create_map(x, y)
