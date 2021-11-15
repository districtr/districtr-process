import json
import logging
import pathlib
import argparse

# from glob import glob
# from multiprocessing import Pool

import yaml
# import requests

from .place import PlaceSchema
from .process import process

logging.captureWarnings(True)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def load(place_filename):
    schema = PlaceSchema()
    place_file = pathlib.Path(place_filename)
    if place_file.suffix == ".yaml" or place_file.suffix == ".yml":
        with open(place_file) as f:
            place = schema.load(yaml.load(f, Loader=yaml.SafeLoader))
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


def many(filenames, output_file, upload=True, overwrite=False):
    # args = [(filename, upload) for filename in filenames]
    records = [main(filename, upload, overwrite) for filename in filenames]
    with open(output_file, "w") as f:
        json.dump(records, f, indent=2)
    # with Pool(8) as pool:
        # records = list(pool.starmap(main, args))
        # print(records)
        # with open(output_file, "w") as f:
            # json.dump(records, f, indent=2)


def main(place_filename, upload=True, overwrite=False):
    print(place_filename)
    place = load(place_filename)

    units_records = [
        process(units, place["id"], upload=upload, overwrite=overwrite) for units in place["units"]
    ]
    place_record = place.copy()
    place_record["units"] = units_records


    place_record["districtingProblems"] = place_record["districting_problems"]
    del place_record["districting_problems"]

    for record in place_record["districtingProblems"]:
        record["numberOfParts"] = record["number_of_parts"]
        del record["number_of_parts"]

        record["pluralNoun"] = record["plural_noun"]
        del record["plural_noun"]

    # place_record["slug"] = place_record["id"]
    # del place_record["id"]

    # for record in place_record["units"]:
        # record["slug"] = record["id"]
        # del record["id"]

    # resp = requests.delete(f"http://localhost:5000/places/{place_record['slug']}")

    # resp = requests.post(
    #     "https://api.districtr.org/places/", json=place_record, headers=HEADERS
    # )
    # print(resp)
    # print(resp.content)

    return place_record


if __name__ == "__main__":
    # places = requests.get("https://api.districtr.org/places/", headers=HEADERS)
    # excluded = [place["slug"] for place in places.json()]
    # excluded = ["alaska", "utah"]
    # filenames = [
    #     filename
    #     for filename in glob("./data/*.yml")
    #     if all(name not in filename for name in excluded)
    # ]

    parser = argparse.ArgumentParser(description="Upload / Create Districtr modules", prog="districtr_process")
    parser.add_argument("files", nargs="+", type=str, help=".yml files corresponding to modules to upload")
    parser.add_argument("--force", action="store_true", help="overwrite existing mbtiles output?")
    parser.add_argument("--upload", action="store_true", help="upload tiles to mapbox?")
    args = parser.parse_args()

    filenames = args.files
    overwrite = args.force
    upload = args.upload
    print(filenames)

    many(filenames, "output.json", upload=upload, overwrite=overwrite)
