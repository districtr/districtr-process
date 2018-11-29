import pathlib
import subprocess
from tempfile import TemporaryDirectory

from .exceptions import TippecanoeError


def tippecanoe_shell_command(filename, place, target, minzoom=0, maxzoom=None):
    accumulate_elections = [
        f"--accumulate-attribute={col.key}:sum"
        for election in place.elections
        for col in election.vote_totals
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


def create_tiles(filename, place, target, tippecanoe_args=None):
    if tippecanoe_args is None:
        tippecanoe_args = {}

    # The GeoDataFrame.to_json method includes ``id`` attributes coming
    # from the Index. So using set_index above gives us the joint index
    target_absolute = str(pathlib.Path(target).absolute())

    command = tippecanoe_shell_command(
        filename, place, target_absolute, **tippecanoe_args
    )
    result = subprocess.run(command)

    return result
