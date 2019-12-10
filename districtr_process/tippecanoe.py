import pathlib
import subprocess


def tippecanoe_shell_command(filename, place, target, minzoom=0, maxzoom=None, 
                             overwrite=False):
    accumulate_columns = [
        f"--accumulate-attribute={col.key}:sum" for col in place.columns
    ]

    zoom_options = ["-Z", str(minzoom)]
    if maxzoom is None:
        zoom_options.append("-zg")
    else:
        zoom_options += ["-z", str(maxzoom)]

    force_options = []
    if overwrite: force_options.append("-f")

    return (
        ["tippecanoe", "-o", target]
        + zoom_options
        + accumulate_columns
        + force_options
        + [
            "--extend-zooms-if-still-dropping",
            "--no-tiny-polygon-reduction",
            "--detect-shared-borders",
            filename
        ]
    )


def create_tiles(filename, units, target, overwrite=False, tippecanoe_args=None):
    if tippecanoe_args is None:
        tippecanoe_args = {}

    target_absolute = str(pathlib.Path(target).absolute())
    source_absolute = str(pathlib.Path(filename).absolute())

    command = tippecanoe_shell_command(
        source_absolute, units, target_absolute, overwrite=overwrite,
        **tippecanoe_args
    )
    print(command)
    result = subprocess.run(command)

    return result
