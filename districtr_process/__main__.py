import json
import logging
import pathlib
from tqdm import tqdm

from glob import glob

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


def fill_in_nones(pairs):
    for pair in pairs:
        if isinstance(pair, tuple) and len(pair) == 2:
            yield pair
        else:
            yield (pair, None)


def many(pairs, output_file, upload=True):
    pairs = list(fill_in_nones(pairs))
    records = [
        main(place_filename=place_filename, shapefile=shapefile, upload=upload)
        for place_filename, shapefile in tqdm(pairs)
    ]
    print(records)
    with open(output_file, "w") as f:
        json.dump(records, f)


def main(place_filename, shapefile=None, upload=True):
    place = load(place_filename)
    if shapefile is None:
        if place.source is not None:
            shapefile = place.source
        else:
            raise ValueError("Must provide a shapefile source")
    place_record = process(shapefile, place, upload=upload)
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
    filenames = glob("./data/*.yml")
    many(filenames, "./output.json", upload=False)
    # print(result)
