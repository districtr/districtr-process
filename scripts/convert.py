from glob import glob
import yaml


def column_sets(data):
    result = []

    if "population" in data:
        population = data["population"]
        population["type"] = "population"
        population["name"] = "Population"
        result.append(population)

    election_sets = [
        {
            "type": "election",
            "metadata": {"year": election["year"], "race": election["race"]},
            "subgroups": election["vote_totals"],
        }
        for election in data.get("elections", [])
    ]

    result += election_sets
    return result


def convert(data):
    new_data = {key: data[key] for key in ["id", "name", "unitType", "idColumn"]}
    new_data["column_sets"] = column_sets(data)
    return new_data


if __name__ == "__main__":
    for filename in glob("./data/*.yml"):
        print(filename)
        with open(filename) as f:
            data = yaml.safe_load(f)
        converted = convert(data)
        with open(filename, "w") as f:
            yaml.dump(converted, f)
