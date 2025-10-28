class Controls:
    def __init__(self, diagram):
        self.diagram = diagram

    def toggle_node_visibility(self, node_id):
        node = self.diagram.get_node(node_id)
        if node:
            node.visible = not node.visible
            self.diagram.update()

    def adjust_edge_distribution(self, edge_id, new_distribution):
        edge = self.diagram.get_edge(edge_id)
        if edge:
            edge.distribution = new_distribution
            self.diagram.update()

    def set_node_size_metric(self, metric):
        for node in self.diagram.nodes:
            node.size_metric = metric
        self.diagram.update()

    def filter_nodes(self, criteria):
        filtered_nodes = [node for node in self.diagram.nodes if criteria(node)]
        self.diagram.update(filtered_nodes)

    def reset_filters(self):
        self.diagram.reset_node_visibility()
        self.diagram.update()