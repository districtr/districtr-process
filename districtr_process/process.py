import json
import pathlib
import tempfile

import geopandas

from .tippecanoe import create_tiles
from .upload import upload

wgs84 = "+init=epsg:4326"


def process(filename, place, upload=True):
    print(place)
    df = read_file(filename, project=upload)

    place.raise_for_problems(df)

    # only keep the data that you need
    df = df[["geometry"] + [col.key for col in place.columns]]

    if place.id_column is not None:
        df.set_index(
            place.id_column.key, inplace=True, drop=False, verify_integrity=True
        )

    if upload:
        with tempfile.TemporaryDirectory() as tempdir:
            print("Generating point geometry")
            save_points(df, place, tempdir)

            mbtiles_filename = "{}/{}.mbtiles".format(tempdir, place.id)

            # Need to catch TippecanoeErrors here
            print("Creating tiles")
            filename = pathlib.Path(tempdir) / "{}.geojson".format(place.id)
            add_id_attribute_and_dump(df, filename)
            result = create_tiles(
                str(filename.absolute()), place, target=mbtiles_filename
            )
            result.check_returncode()

            print("Uploading to Mapbox")
            upload_response = upload(mbtiles_filename, place.id)
            print(upload_response.json())

    # TODO: Create database records.
    return place.record(df)


def save_points(df, place, target_dir):
    points_filename = "{}/{}_points.geojson".format(target_dir, place.id)
    add_id_attribute_and_dump(points(df), points_filename)
    print("Uploading points")
    upload_response = upload(points_filename, place.id + "_points")
    print(upload_response.json())


def add_id_attribute_and_dump(df, filename):
    geojson = convert_id_attribute_to_int(df.__geo_interface__)
    with open(filename, "w") as f:
        json.dump(geojson, f)


def read_file(filename, project=True):
    df = geopandas.read_file(filename)
    if project and df.crs != wgs84:
        df.to_crs(wgs84, inplace=True)
    return df


def points(df):
    assert df.crs == wgs84
    points = df.copy()
    points.geometry = df.geometry.representative_point()
    return points


def convert_to_integer_ids(ids):
    """Given unique IDs, returns a dictionary from those IDs to unique
    integer IDs.
    :param ids: container of ids. The ids must be sortable.
    """
    if len(ids) != len(set(ids)):
        raise ValueError("The given IDs are not unique")
    integer_id_lookup = dict((id, i) for i, id in enumerate(sorted(ids)))
    return integer_id_lookup


def add_id_attribute_from_property(geojson, id_property, lookup=None):
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


def convert_id_attribute_to_int(geojson):
    features = geojson["features"]

    ids = [f["id"] for f in features]

    lookup = convert_to_integer_ids(ids)

    for i, feature in enumerate(features):
        feature["id"] = lookup[feature["id"]]

    return geojson
