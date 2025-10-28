import unittest
from sankey_interactive.core.diagram import Diagram
from sankey_interactive.core.node import Node
from sankey_interactive.core.edge import Edge

class TestDiagram(unittest.TestCase):
    def setUp(self):
        self.diagram = Diagram()

    def test_add_node(self):
        node = Node(id='A', size=10)
        self.diagram.add_node(node)
        self.assertIn(node, self.diagram.nodes)

    def test_add_edge(self):
        node_a = Node(id='A', size=10)
        node_b = Node(id='B', size=20)
        self.diagram.add_node(node_a)
        self.diagram.add_node(node_b)
        edge = Edge(source=node_a, target=node_b, width=5)
        self.diagram.add_edge(edge)
        self.assertIn(edge, self.diagram.edges)

    def test_node_metrics(self):
        node = Node(id='A', size=10)
        self.diagram.add_node(node)
        node.update_metrics(size=15)
        self.assertEqual(node.size, 15)

    def test_edge_metrics(self):
        node_a = Node(id='A', size=10)
        node_b = Node(id='B', size=20)
        edge = Edge(source=node_a, target=node_b, width=5)
        edge.update_metrics(width=10)
        self.assertEqual(edge.width, 10)

if __name__ == '__main__':
    unittest.main()