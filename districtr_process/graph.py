from gerrychain import Graph


def save_graph(place, filename):
    print("Creating rook graph")
    rook = Graph.from_file(
        filename, adjacency="rook", columns=[col.key for col in place.columns]
    )
    rook.to_json("./graphs/{}_rook.json".format(place.id))

    print("Creating queen graph")
    queen = Graph.from_file(
        filename, adjacency="queen", columns=[col.key for col in place.columns]
    )
    queen.to_json("./graphs/{}_queen.json".format(place.id))
