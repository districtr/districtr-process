from gerrychain import Graph


def save_graph(place, filename):
    graph = Graph.from_file(filename, columns=[col.key for col in place.columns])
    graph.to_json("./graphs/{}.json".format(place.id))
