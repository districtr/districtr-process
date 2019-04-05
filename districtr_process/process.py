import logging

import geopandas

from .tileset import Tileset

wgs84 = "+init=epsg:4326"

log = logging.getLogger(__name__)


def process(units, place_id, upload=True):
    log.info("Processing %s_%s", place_id, units.id)
    df = read_file(units.source, project=upload)

    points_tileset = Tileset(points(df), units, f"{place_id}_{units.id}_points")
    polygons_tileset = Tileset(df, units, f"{place_id}_{units.id}")

    if upload:
        assert df.crs == wgs84
        points_tileset.upload()
        polygons_tileset.upload()

    record = units.record(df)
    record["tilesets"] = [polygons_tileset.record(), points_tileset.record()]
    return record


def read_file(filename, project=True):
    df = geopandas.read_file(filename)
    if project and df.crs != wgs84:
        df.to_crs(wgs84, inplace=True)
    return df


def points(df):
    points = df.copy()
    points.geometry = df.geometry.representative_point()
    return points
