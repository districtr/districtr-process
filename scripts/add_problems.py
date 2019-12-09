import json
from glob import glob
import yaml


def get_problems_by_name(response_file):
    with open(response_file) as f:
        response = json.load(f)

    def get_name(place):
        return place.get("permalink", place.get("id"))

    name_to_problems = {
        get_name(place): place["districtingProblems"] for place in response
    }
    assert all(isinstance(key, str) for key in name_to_problems)
    return name_to_problems


def add_problems(name_to_problems):
    for filename in glob("./data/*.yml"):
        print(filename)
        with open(filename) as f:
            record = yaml.safe_load(f)
        problems = name_to_problems[record["id"]]
        record["districtingProblems"] = problems
        with open(filename, "w") as f:
            yaml.safe_dump(record, f)


if __name__ == "__main__":
    name_to_problems = get_problems_by_name("../districtr/assets/data/response.json")
    add_problems(name_to_problems)
