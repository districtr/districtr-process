from districtr_process.process import read_in_wgs84, wgs84


def test_wgs84_works(shapefile):
    assert read_in_wgs84(shapefile).crs == wgs84


def test_to_crs_does_nothing_if_already_in_the_requested_crs(geodataframe):
    assert all(geodataframe.to_crs(wgs84).geometry.geom_equals(geodataframe.geometry))
