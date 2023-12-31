from .graph import Graph, nx, plt


class WattsStrogatz(Graph):
    def __init__(self, n, k, p, **attr) -> None:
        super().__init__(**attr)
        g = nx.watts_strogatz_graph(n, k, p, seed=self.seed)
        self.add_nodes_from(g.nodes)
        self.add_edges_from(g.edges)


def main() -> None:
    ba = WattsStrogatz(100, 2, 0.1)
    ba.draw()
    plt.show()
    ba.histogram()
    ba.mark_shortest_path(1, 98)
    print(ba.get_largest_components_size())


if __name__ == "__main__":
    main()
