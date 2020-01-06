from sys import argv
import json

# pip install fiona shapely shapely-geojson
import fiona
from shapely.geometry import shape
from shapely_geojson import dumps

if len(argv) < 2:
    print('usage: gen_map.py "New Mexico"')
    quit()
target_state = argv[1]
states = []
for pol in fiona.open('tl_2019_us_state/tl_2019_us_state.shp'):
    name = pol['properties']['NAME']
    if name == target_state:
        states.append(shape(pol['geometry']))

features = {
    "type": "FeatureCollection",
    "features": []
}
for pol in fiona.open('tl_2019_us_aiannh/tl_2019_us_aiannh.shp'):
    geo = shape(pol['geometry'])
    for state in states:
        if geo.intersects(state):
            features["features"].append({
                "geometry": json.loads(dumps(geo)),
                "properties": pol['properties']
            })
            break
print(json.dumps(features, separators=(',', ':')))
