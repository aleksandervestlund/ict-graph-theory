from .graph import Graph, nx


class StarGraph(Graph):
    def __init__(self, n, **attr) -> None:
        super().__init__(**attr)
        g = nx.star_graph(n)
        self.add_nodes_from(g.nodes)
        self.add_edges_from(g.edges)
