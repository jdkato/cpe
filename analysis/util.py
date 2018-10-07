import geopandas
import pandas

from cycler import cycler
from matplotlib import pyplot

from pathlib import Path
from typing import List, Dict, Callable

DATA = Path('analysis/data')


def plot_dist_composition(dists: Path, tracts: Path, d_id: int):
    """Plot the Census Tracts that compose the police district `d_id`.
    """
    fig, axis = pyplot.subplots()

    police_gdf, tracts_gdf, comp = dist_composition(dists, tracts, d_id)

    name = police_gdf["Name"][d_id]
    dist = shrink_gdf(police_gdf, lambda i, e: i == d_id)
    dist.plot(ax=axis, column='Name')

    for tract in comp:
        t_gdf = shrink_gdf(tracts_gdf, lambda i, e: e["GEOID"] == tract)

        t_gdf.apply(lambda x: axis.annotate(
            text=tract[-4:],
            xy=x.geometry.centroid.coords[0],
            ha='center'), axis=1)

        t_gdf.plot(
            ax=axis,
            color="#d3d3d3",
            alpha=.4,
            edgecolor="#a8a8a8")

    pyplot.title("Census Tracts in '{0}'".format(name))
    pyplot.axis("off")
    pyplot.show()


def data_for_dept(dept: str, pat: str) -> List[Path]:
    """Return the files with names that match `pat` for `dept`.
    """
    target = None
    for entry in DATA.iterdir():
        if entry.is_dir() and entry.name == dept:
            target = entry
            break
    return list(target.glob(pat))


def dist_composition(dists: Path, tracts: Path, d_id: int) -> Dict[str, float]:
    """Return the Census Tract composition for the given district.
    """
    tract_gdf = geopandas.read_file(str(tracts))
    dists_gdf = geopandas.read_file(str(dists))
    if tract_gdf.crs != dists_gdf.crs:
        t_epsg = int(tract_gdf.crs['init'].split(':')[1])
        dists_gdf = dists_gdf.to_crs(epsg=t_epsg)

    dist = list(dists_gdf.iterrows())[d_id]
    comp = {}
    for idx, tract in tract_gdf.iterrows():
        if tract["geometry"].intersects(dist[1]["geometry"]):
            area = tract["geometry"].intersection(dist[1]["geometry"]).area
            t_id = tract["GEOID"]
            comp[t_id] = round((area / tract['geometry'].area) * 100, 3)

    return dists_gdf, tract_gdf, comp


def shrink_gdf(gdf: geopandas.GeoDataFrame, f: Callable) -> geopandas.GeoDataFrame:
    """Isolate a given entry in a GeoDataFrame.
    """
    data = []
    for i, entry in gdf.iterrows():
        if f(i, entry):
            data.append(entry)
            break
    return geopandas.GeoDataFrame(pandas.DataFrame(data))
