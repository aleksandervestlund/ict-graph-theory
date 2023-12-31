from lxml import etree
import requests

from .graph import Graph, nx, plt


class RealNetworkGraph(Graph):
    def __init__(self, url: str, **attr) -> None:
        super().__init__(**attr)
        r = requests.get(url)
        tree = etree.XML(r.content)
        graph = tree.find("{http://graphml.graphdrawing.org/xmlns}graph")
        nodes = graph.findall("{http://graphml.graphdrawing.org/xmlns}node")
        edges = graph.findall("{http://graphml.graphdrawing.org/xmlns}edge")
        self.graph_nodes = [
            {"id": n.attrib["id"], "label": n.getchildren()[-1].text}
            for n in nodes
        ]
        self.graph_edges = [
            (e.attrib["source"], e.attrib["target"]) for e in edges
        ]
        self._init_nodes()
        self._init_edges()

    def _init_nodes(self) -> None:
        for node in self.graph_nodes:
            self.add_node(node["id"], label=node["label"])

    def _init_edges(self) -> None:
        self.add_edges_from(self.graph_edges)

    def draw(
        self,
        edge_color: str = "#b4b4b4",
        node_color: str = "k",
        figsize: tuple[int, int] = (15, 14),
        with_labels: bool = True,
        font_size: int = 10,
        node_size: int = 20,
        edge_width: float = 0.6,
    ) -> None:
        plt.figure(num=None, figsize=figsize)
        labels = (
            {n["id"]: n["label"] for n in self.graph_nodes}
            if with_labels
            else None
        )

        nx.draw_kamada_kawai(
            self,
            labels=labels,
            node_size=node_size,
            font_size=font_size,
            with_labels=with_labels,
            edge_color=edge_color,
            node_color=node_color,
            width=edge_width,
            linewidths=0,
            alpha=1,
        )
        plt.show()


def main() -> None:
    rn = RealNetworkGraph(
        "http://www.topology-zoo.org/files/Uninett2011.graphml"
    )
    rn.draw()


if __name__ == "__main__":
    main()
