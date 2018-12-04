from tempfile import TemporaryDirectory

from districtr_process.place import Place
from districtr_process.tippecanoe import create_tiles


def test_create_tiles(geojson):
    place = Place("1234", "My place")
    with TemporaryDirectory() as tempdir:
        result = create_tiles(geojson, place, target=tempdir + "/temp.mbtiles")
    assert result.returncode == 0
