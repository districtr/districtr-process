import json
import logging
import pathlib
import sys

import yaml

from .place import PlaceSchema
from .process import process

logging.captureWarnings(True)


def load(place_filename):
    schema = PlaceSchema()
    place_file = pathlib.Path(place_filename)
    if place_file.suffix == ".yaml" or place_file.suffix == ".yml":
        with open(place_file) as f:
            place = schema.load(yaml.load(f))
    elif place_file.suffix == ".json":
        with open(place_file) as f:
            place = schema.load(json.load(f))
    else:
        raise TypeError("The given place filename is not in yaml or json format")
    return place


def many(pairs, output_file):
    records = [main(filename, place_filename) for filename, place_filename in pairs]
    print(records)
    with open(output_file, "w") as f:
        json.dump(records, f)


def main(filename, place_filename):
    place = load(place_filename)
    place_record = process(filename, place)
    return place_record


def find_shp(folder):
    for item in folder.iterdir():
        if item.suffix == ".shp":
            return str(item.absolute())


if __name__ == "__main__":
    # with open("./places.txt") as f:
    #     args = [tuple(line.strip().split(" ")) for line in f if line[0] != "#"]
    # pairs = [
    #     (
    #         find_shp(pathlib.Path(f"./shapes/{shapefile_folder}")),
    #         f"./data/{place_name}.yml",
    #     )
    #     for place_name, shapefile_folder in args
    # ]
    # many(pairs, "./output.json")
    # result = main(*sys.argv[1:3])
    result = many([tuple(sys.argv[1:3])], "./output.json")
    print(result)
