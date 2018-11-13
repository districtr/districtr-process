def tippecanoe_shell_command(spec, filename, minzoom=0, maxzoom=14):
    accumulate_elections = [
        f"--accumulate-attribute={col}:sum"
        for election in spec.elections
        for col in election.parties_to_columns
    ]
    accumulate_population = f"--accumulate-attribute={spec.population.total}"
    return (
        [
            "tippecanoe",
            "-o",
            f"{spec.id}.mbtiles",
            "-Z",
            minzoom,
            "-z",
            maxzoom,
            "--generate-ids",
        ]
        + accumulate_elections
        + accumulate_population
        + ["--coalesce-densest-as-needed", "--extend-zooms-if-still-dropping", filename]
    )
