class Filters:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def filter_nodes(self, criteria):
        """Filter nodes based on user-defined criteria."""
        return [node for node in self.nodes if self._matches_criteria(node, criteria)]

    def filter_edges(self, criteria):
        """Filter edges based on user-defined criteria."""
        return [edge for edge in self.edges if self._matches_criteria(edge, criteria)]

    def _matches_criteria(self, item, criteria):
        """Check if the item matches the given criteria."""
        for key, value in criteria.items():
            if getattr(item, key, None) != value:
                return False
        return True

    def reset_filters(self):
        """Reset filters to show all nodes and edges."""
        return self.nodes, self.edges