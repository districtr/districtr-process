import pathlib
import subprocess
from tempfile import TemporaryDirectory

from .exceptions import TippecanoeError


def tippecanoe_shell_command(filename, place, target, minzoom=0, maxzoom=14):
    accumulate_elections = [
        f"--accumulate-attribute={col}:sum"
        for election in place.elections
        for col in election.parties_to_columns
    ]

    accumulate_population = []
    if place.population is not None:
        accumulate_population = [
            f"--accumulate-attribute={place.population.total}:sum"
        ] + [f"--accumulate-attribute={col}:sum" for col in place.population.subgroups]

    zoom_options = ["-Z", str(minzoom)]
    if maxzoom is None:
        zoom_options.append("-zg")
    else:
        zoom_options += ["-z", str(maxzoom)]

    return (
        ["tippecanoe", "-o", target]
        + zoom_options
        + accumulate_elections
        + accumulate_population
        + ["--coalesce-densest-as-needed", "--extend-zooms-if-still-dropping", filename]
    )


def create_tiles(df, place, target, tippecanoe_args=None):
    if tippecanoe_args is None:
        tippecanoe_args = {}

    # The GeoDataFrame.to_json method includes ``id`` attributes coming
    # from the Index. So using set_index above gives us the joint index
    geojson = df.to_json()

    target_absolute = str(pathlib.Path(target).absolute())

    with TemporaryDirectory() as tempdir:
        filename = pathlib.Path(tempdir) / "{}.json".format(place.id)
        filename_absolute = str(filename.absolute())
        with open(filename_absolute, "w") as f:
            f.write(geojson)
        print(filename_absolute, target_absolute)
        command = tippecanoe_shell_command(
            filename_absolute, place, target_absolute, **tippecanoe_args
        )
        result = subprocess.run(command)

    return result
