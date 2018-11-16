import tempfile

import geopandas

from .tippecanoe import create_tiles

wgs84 = "+init=epsg:4326"


def process(filename, place):
    df = read_in_wgs84(filename)
    with tempfile.TemporaryDirectory() as tempdir:
        geojson_filename = "{}/{}.geojson".format(tempdir, place.id)
        write_as_geojson(df, geojson_filename)

        centroids_filename = "{}/{}-centroids.geojson".format(tempdir, place.id)
        create_centroid_geojson(df, centroids_filename)

        mbtiles_filename = "{}.{}.mbtiles".format(tempdir, place.id)
        create_tiles(geojson_filename, place, target=mbtiles_filename)


def read_in_wgs84(filename):
    df = geopandas.read_file(filename)
    if df.crs != wgs84:
        df.to_crs(wgs84, inplace=True)
    return df


def create_centroid_geojson(df, target):
    assert df.crs == wgs84
    centroids = df.copy()
    centroids.geometry = df.centroid
    centroids.to_file(target, driver="GeoJSON")


def write_as_geojson(df, target):
    df.to_crs(wgs84).to_file(target, driver="GeoJSON")
