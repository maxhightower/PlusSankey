from typing import List, Dict

class NodeMetrics:
    def __init__(self, node_data: List[Dict]):
        self.node_data = node_data

    def calculate_sizes(self) -> List[float]:
        """Calculate sizes for nodes based on some metrics."""
        sizes = []
        for node in self.node_data:
            size = self._compute_size(node)
            sizes.append(size)
        return sizes

    def _compute_size(self, node: Dict) -> float:
        """Compute size for a single node."""
        # Example metric: size based on a property 'value'
        return node.get('value', 1) * 10  # Adjust multiplier as needed

    def adjust_node_sizes(self, scaling_factor: float) -> List[float]:
        """Adjust node sizes by a scaling factor."""
        sizes = self.calculate_sizes()
        adjusted_sizes = [size * scaling_factor for size in sizes]
        return adjusted_sizes

    def filter_nodes(self, criteria: Dict) -> List[Dict]:
        """Filter nodes based on given criteria."""
        filtered_nodes = [
            node for node in self.node_data
            if all(node.get(key) == value for key, value in criteria.items())
        ]
        return filtered_nodes

    def get_node_metrics(self) -> Dict[str, float]:
        """Get metrics for all nodes."""
        metrics = {
            'total_nodes': len(self.node_data),
            'average_size': sum(self.calculate_sizes()) / len(self.node_data) if self.node_data else 0,
        }
        return metrics