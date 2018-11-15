import pathlib
from tempfile import TemporaryDirectory

import geopandas as gp
import pytest
from shapely.geometry import Polygon


@pytest.fixture
def geodataframe():
    a = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    b = Polygon([(0, 1), (0, 2), (1, 2), (1, 1)])
    c = Polygon([(1, 0), (1, 1), (2, 1), (2, 0)])
    d = Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])
    df = gp.GeoDataFrame({"ID": ["a", "b", "c", "d"], "geometry": [a, b, c, d]})
    df.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
    return df


@pytest.fixture
def gdf_with_data(geodataframe):
    geodataframe["data"] = list(range(len(geodataframe)))
    geodataframe["data2"] = list(range(len(geodataframe)))
    return geodataframe


@pytest.fixture
def geodataframe_with_boundary():
    """
    abe
    ade
    ace
    """
    a = Polygon([(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 2), (1, 1), (1, 0)])
    b = Polygon([(1, 2), (1, 3), (2, 3), (2, 2)])
    c = Polygon([(1, 0), (1, 1), (2, 1), (2, 0)])
    d = Polygon([(1, 1), (1, 2), (2, 2), (2, 1)])
    e = Polygon([(2, 0), (2, 1), (2, 2), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0)])
    df = gp.GeoDataFrame({"ID": ["a", "b", "c", "d", "e"], "geometry": [a, b, c, d, e]})
    df.crs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
    return df


@pytest.fixture
def shapefile(gdf_with_data):
    with TemporaryDirectory() as d:
        filepath = pathlib.Path(d) / "temp.shp"
        filename = str(filepath.absolute())
        gdf_with_data.to_file(filename)
        yield filename
