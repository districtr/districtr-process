import logging

import geopandas
import pandas as pd

from .tileset import Tileset

wgs84 = "+init=epsg:4326"

log = logging.getLogger(__name__)


def process(units, place_id, upload=True, overwrite=False, project=True):
    log.info("Processing %s_%s", place_id, units.id)
    df = read_file(units.source, project=project)
    
    points_tileset = Tileset(points(df), units, f"{place_id}_{units.id}_points")
    polygons_tileset = Tileset(df, units, f"{place_id}_{units.id}")

    if upload:
        # assert df.crs == wgs84
        points_tileset.upload(overwrite=overwrite)
        polygons_tileset.upload(overwrite=overwrite)

    record = units.record(df)
    record["tilesets"] = [polygons_tileset.record(), points_tileset.record()]

    return record


def read_file(filename, project=True):
    df = geopandas.read_file(filename)
    if filename == "./shapes/LA_precincts_VRA/LA_final.shp":
        elec_columns = list(pd.read_csv("./shapes/LA_precincts_VRA/LA_column_names.csv")["new"])
        df.columns = df.columns.str.replace("-", "_")
        state_gdf_cols = list(df.columns)
        cand1_index = state_gdf_cols.index('DeatonD_15')
        cand2_index = state_gdf_cols.index('WolfeD_16P')
        state_gdf_cols[cand1_index:cand2_index+1] = elec_columns
        df.columns = state_gdf_cols
        df['LandrieuI_19P_Governor'] = df['LandrieuI_19P_Governor'].astype(float)

    if project and df.crs != wgs84:
        df.to_crs(wgs84, inplace=True)
    return df


def points(df):
    points = df.copy()
    points.geometry = df.geometry.representative_point()
    return points
