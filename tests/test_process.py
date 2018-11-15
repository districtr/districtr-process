from process import read_in_wgs84, wgs84


def test_wgs84_equality_works(shapefile):
    assert read_in_wgs84(shapefile).crs == wgs84
