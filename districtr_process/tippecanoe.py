import pathlib
import subprocess


def tippecanoe_shell_command(filename, place, target, minzoom=0, maxzoom=None):
    accumulate_columns = [
        f"--accumulate-attribute={col.key}:sum" for col in place.columns
    ]

    zoom_options = ["-Z", str(minzoom)]
    if maxzoom is None:
        zoom_options.append("-zg")
    else:
        zoom_options += ["-z", str(maxzoom)]

    return (
        ["tippecanoe", "-o", target]
        + zoom_options
        + accumulate_columns
        + ["--coalesce-densest-as-needed", "--extend-zooms-if-still-dropping", filename]
    )


def create_tiles(filename, place, target, tippecanoe_args=None):
    if tippecanoe_args is None:
        tippecanoe_args = {}

    target_absolute = str(pathlib.Path(target).absolute())
    source_absolute = str(pathlib.Path(filename).absolute())

    command = tippecanoe_shell_command(
        source_absolute, place, target_absolute, **tippecanoe_args
    )
    result = subprocess.run(command)

    return result
