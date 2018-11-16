import pytest

from districtr_process.process import convert_to_integer_ids, read_in_wgs84, wgs84


def test_wgs84_works(shapefile):
    assert read_in_wgs84(shapefile).crs == wgs84


def test_to_crs_does_nothing_if_already_in_the_requested_crs(geodataframe):
    assert all(geodataframe.to_crs(wgs84).geometry.geom_equals(geodataframe.geometry))


def test_series_can_be_converted_to_ids(geodataframe):
    lookup = convert_to_integer_ids(geodataframe["ID"])
    assert all(key in lookup for key in geodataframe["ID"])
    assert set(lookup.values()) == set(range(len(geodataframe["ID"])))


def test_ids_must_be_unique():
    with pytest.raises(ValueError):
        convert_to_integer_ids(["same", "same", "same"])
