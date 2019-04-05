from tempfile import TemporaryDirectory

from districtr_process.place import Units
from districtr_process.tippecanoe import create_tiles


def test_create_tiles(geojson):
    units = Units("1234", "My place")
    with TemporaryDirectory() as tempdir:
        result = create_tiles(geojson, units, target=tempdir + "/temp.mbtiles")
    assert result.returncode == 0
