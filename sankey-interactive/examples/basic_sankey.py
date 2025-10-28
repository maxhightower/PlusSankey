from sankey_interactive.core.diagram import Diagram
from sankey_interactive.core.node import Node
from sankey_interactive.core.edge import Edge

def main():
    # Create a new Sankey diagram
    sankey_diagram = Diagram()

    # Add nodes
    node_a = Node(name="Node A", size=10)
    node_b = Node(name="Node B", size=20)
    sankey_diagram.add_node(node_a)
    sankey_diagram.add_node(node_b)

    # Add an edge between the nodes
    edge_ab = Edge(source=node_a, target=node_b, width=5)
    sankey_diagram.add_edge(edge_ab)

    # Render the diagram
    sankey_diagram.render()

if __name__ == "__main__":
    main()