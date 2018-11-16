import subprocess


def tippecanoe_shell_command(filename, place, target, minzoom=0, maxzoom=14):
    accumulate_elections = [
        f"--accumulate-attribute={col}:sum"
        for election in place.elections
        for col in election.parties_to_columns
    ]
    accumulate_population = [f"--accumulate-attribute={place.population.total}:sum"] + [
        f"--accumulate-attribute={col}:sum" for col in place.population.subgroups
    ]
    zoom_options = ["-Z", minzoom, "-z", maxzoom]
    return (
        ["tippecanoe", "-o", target]
        + zoom_options
        + accumulate_elections
        + accumulate_population
        + ["--coalesce-densest-as-needed", "--extend-zooms-if-still-dropping", filename]
    )


def create_tiles(filename, place, target, tippecanoe_args):
    command = tippecanoe_shell_command(filename, place, **tippecanoe_args)
    subprocess.run(command)
