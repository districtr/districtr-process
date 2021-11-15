
import json
from sys import argv

fin, fout = argv[-2], argv[-1]

# Read in the data.
with open(fin) as f: data = json.load(f)

# Helper functions.
def find_bg_module(name):
    def _(module):
        if module["name"] == name and module["units"][0]["unitType"] == "Block Groups":
            return module

    return _

# Identify each of the block-level modules.
cities = [c for c in data if c["units"][0]["unitType"] == "Blocks"]

# For each of the city modules, add the block group tileset to its array of tilesets.
for city in cities:
    try:
        bg_module = list(filter(find_bg_module(city["name"]), data))[0]
    except:
        print(f"A block group tileset for {city['name']} couldn't be found; skipping.")
        continue

    # Get the tileset from the module.
    bg_tileset = bg_module["units"][0]["tilesets"][0]
    city["units"][0]["tilesets"].append(bg_tileset)


# For each of the city modules, get the Percentages column set from the block 
# group module.
for city in cities:
    try:
        bg_module = list(filter(find_bg_module(city["name"]), data))[0]
    except:
        print(f"A block group tileset for {city['name']} couldn't be found; skipping.")
        continue

    bg_percentages = bg_module["units"][0]["columnSets"][0]

    # Adjust subgroup properties.
    for subgroup in bg_percentages["subgroups"]:
        subgroup["name"] = subgroup["name"].split(" percent")[0]
        if subgroup["key"] == "Inc75": subgroup["name"] = ">$75K income"
        if not subgroup["max"]: subgroup["max"] = 1

    # Move the "child at home" to the top instead of "total population."
    child_at_home = bg_percentages["subgroups"][0]
    bg_percentages["subgroups"] = bg_percentages["subgroups"][1:]
    bg_percentages["name"] = "Percentages"
    bg_percentages["total"] = child_at_home

    city["units"][0]["columnSets"].append(bg_percentages)

# Set the "name" of each block unit to "2020 Blocks"
for city in cities: city["units"][0]["name"] = "2020 Blocks"

# Print the id for each city for referencing later.
for city in cities: print(city["id"])

# Write to file.
with open(fout, "w") as f: json.dump(cities, f, indent=2)
