def get_network(seed: int = 246) -> str:
    with open(
        "graph_utils/real_graph_alternatives.txt", encoding="utf-8"
    ) as f:
        graphs = f.readlines()
        g = graphs[seed]
        g_name = g.split(".")[0]
        print(f"You will analyze the {g_name} network.")
        print(
            f"Your network graph file is http://www.topology-zoo.org/files/{g}"
        )
        return f"http://www.topology-zoo.org/files/{g}".strip("\n")
