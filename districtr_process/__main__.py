import json
import pathlib
import sys

import yaml

from .place import PlaceSchema
from .process import process


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


def main(filename, place_filename):
    place = load(place_filename)
    process(filename, place)


if __name__ == "__main__":
    print(*sys.argv[1:3])
    main(*sys.argv[1:3])
