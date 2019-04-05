import json
import logging
import pathlib
import tempfile

from .tippecanoe import create_tiles
from .upload import upload


log = logging.getLogger(__name__)


class Tileset:
    def __init__(self, df, units, upload_id):
        units.raise_for_problems(df)

        # only keep the data that you need
        self.df = df[[df.geometry.name] + [col.key for col in units.columns]]

        if units.id_column is not None:
            self.df.set_index(
                units.id_column.key, inplace=True, drop=False, verify_integrity=True
            )

        self.units = units

    def upload(self):
        with tempfile.TemporaryDirectory() as tempdir:
            mbtiles_filename = "{}/{}.mbtiles".format(tempdir, self.upload_id)

            log.info("Creating tiles in %s", mbtiles_filename)
            filename = pathlib.Path(tempdir) / "{}.geojson".format(self.upload_id)
            add_id_attribute_and_dump(self.df, filename)

            result = create_tiles(
                str(filename.absolute()), self.units, target=mbtiles_filename
            )
            result.check_returncode()

            log.info("Uploading %s to Mapbox", self.upload_id)
            upload_response = upload(mbtiles_filename, self.upload_id)
            log.info("Upload response: %s", upload_response.json())


def add_id_attribute_and_dump(df, filename):
    geojson = convert_id_attribute_to_int(df.__geo_interface__)
    with open(filename, "w") as f:
        json.dump(geojson, f)


def convert_to_integer_ids(ids):
    """Given unique IDs, returns a dictionary from those IDs to unique
    integer IDs.
    :param ids: container of ids. The ids must be sortable.
    """
    if len(ids) != len(set(ids)):
        raise ValueError("The given IDs are not unique")
    integer_id_lookup = dict((id, i) for i, id in enumerate(sorted(ids)))
    return integer_id_lookup


def convert_id_attribute_to_int(geojson):
    features = geojson["features"]

    ids = [f["id"] for f in features]

    lookup = convert_to_integer_ids(ids)

    for i, feature in enumerate(features):
        feature["id"] = lookup[feature["id"]]

    return geojson
