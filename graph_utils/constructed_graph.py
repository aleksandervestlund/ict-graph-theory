from .graph import Graph, nx


class ConstructedGraph(Graph):
    def __init__(self, expanded=False, **attr) -> None:
        super().__init__(**attr)
        grid_size = 3
        g = nx.grid_2d_graph(grid_size, grid_size)
        f = nx.cycle_graph(6)  # endret fra 5

        def create_mapping(grid_size) -> dict[tuple[int, int], str]:
            mapping: dict[tuple[int, int], str] = {
                (0, 0): "a0",
                (0, 2): "b0",
                (2, 0): "c0",
                (1, 2): "d0",
            }  # endret fra (1,2) på c0
            for i in range(grid_size):
                for j in range(grid_size):
                    if (i, j) not in mapping:
                        mapping[(i, j)] = f"core{i * 3 + j}"
            return mapping

        mapping = create_mapping(grid_size)
        g = nx.relabel_nodes(g, mapping)

        def make_mapping(graph, prefix) -> dict[str, str]:
            mapping = {}
            for elem in graph.nodes:
                mapping[elem] = f"{prefix}{elem}"
            return mapping

        stars = "abcd"
        star_form_list = []
        for letter in stars:
            f_ = nx.relabel_nodes(f, make_mapping(f, letter))
            star_form_list.append(f_)

        access_net_size = 5
        a = nx.star_graph(access_net_size)
        access_net_list = []
        for i, letter in enumerate(stars):
            a_ = nx.relabel_nodes(a, make_mapping(a, stars[0] + letter))
            access_net_list.append(a_)

        for i, letter in enumerate(stars):
            a_ = nx.relabel_nodes(a, make_mapping(a, stars[1] + letter))
            access_net_list.append(a_)

        for i, net in enumerate(access_net_list):
            if i < len(access_net_list) // 2:
                access_net_list[i] = nx.relabel_nodes(
                    net, {list(net.nodes)[1]: list(net.nodes)[2][1:]}
                )
            else:
                access_net_list[i] = nx.relabel_nodes(
                    net, {list(net.nodes)[1]: list(net.nodes)[3][1:]}
                )

        for graph in star_form_list:
            g = nx.compose(g, graph)

        for graph in access_net_list:
            g = nx.compose(g, graph)

        if expanded:
            # adding last part of access nett
            access_sub_net_size = 2
            a_sub = nx.star_graph(access_sub_net_size)
            access_sub_net_list = []
            for i, graph in enumerate(access_net_list):
                for node in list(graph.nodes)[2:]:
                    mapping = make_mapping(a_sub, node)
                    mapping[0] = node  # type: ignore
                    a_sub_ = nx.relabel_nodes(a_sub, mapping=mapping)
                    access_sub_net_list.append(a_sub_)

            for graph in access_sub_net_list:
                g = nx.compose(g, graph)

        self.add_nodes_from(g.nodes)
        self.add_edges_from(g.edges)

        self.add_edge("bb0", "b4")
        self.add_edge("core1", "d0")
        self.add_edge("core3", "b0")
        self.add_edge("d1", "core8")
        self.add_edge("b1", "ab0")  #
        self.remove_edge("b0", "d0")
        self.remove_edge("b0", "core1")
