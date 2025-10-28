"""Interactive Sankey Diagram Library"""

__version__ = "0.1.0"

from .core.diagram import SankeyDiagram
from .core.node import Node
from .core.edge import Edge

__all__ = ["SankeyDiagram", "Node", "Edge"]