import os
import tempfile

import geopandas

from .tippecanoe import create_tiles
from .upload import MapboxError, upload

wgs84 = "+init=epsg:4326"

CENTROIDS_DIR = os.environ.get("CENTROIDS_DIR", None)


def process(filename, place):
    df = read_in_wgs84(filename)

    place.raise_for_problems(df)

    if place.id_column is not None:
        df.set_index(
            place.id_column.key, inplace=True, drop=False, verify_integrity=True
        )

    with tempfile.TemporaryDirectory() as tempdir:
        save_centroids(df, CENTROIDS_DIR or tempdir)

        # The GeoDataFrame.to_json method includes ``id`` attributes coming
        # from the Index. So using set_index above gives us the joint index
        geojson = df.to_json()

        mbtiles_filename = "{}/{}.mbtiles".format(tempdir, place.id)

        # Need to catch TippecanoeErrors here
        create_tiles(geojson, place, target=mbtiles_filename)

        upload_response = upload(geojson_filename, place.id)

        # TODO: put the centroids somewhere. Create database records.


def save_centroids(df, target_dir):
    centroids_filename = "{}/{}-centroids.geojson".format(target_dir, place.id)
    with open(centroids_filename, "w") as f:
        f.write(centroids(df).to_json())


def read_in_wgs84(filename):
    df = geopandas.read_file(filename)
    if df.crs != wgs84:
        df.to_crs(wgs84, inplace=True)
    return df


def centroids(df):
    assert df.crs == wgs84
    centroids = df.copy()
    centroids.geometry = df.centroid
    return centroids


def convert_to_integer_ids(ids):
    """Given unique IDs, returns a dictionary from those IDs to unique
    integer IDs.
    :param ids: container of ids. The ids must be sortable.
    """
    if len(ids) != len(set(ids)):
        raise ValueError("The given IDs are not unique")
    integer_id_lookup = dict((id, i) for i, id in enumerate(sorted(ids)))
    return integer_id_lookup


def add_id_attribute(geojson, id_property, lookup=None):
    """Add an integer ``id`` attribute to a GeoJSON FeatureCollection.
    If a ``lookup`` dictionary is provided, it is used to associate ids to features,
    using the feature's ``id_property`` as a key.
    If it is not provided, converts the given ``id_property`` to integer ids.
    Operates in-place on the ``geojson`` dictionary.

    :param dict geojson: A deserialized GeoJSON object
    :param str id_property: The string key for the property containing unique
        identifiers for all the features.
    :param lookup: (optional) Maps each feature's ``id_property`` value to the 
        desired ``id`` attribute
    :type lookup: dict(str, int)
    :raises ValueError: if the the ``id_property`` values are not unique
    """
    features = geojson["features"]

    if lookup is None:
        ids = [f["properties"][id_property] for f in features]
        lookup = convert_to_integer_ids(ids)

    for feature in features:
        feature["id"] = lookup[feature["properties"][id_property]]

    return geojson
