"""Edge representation for Sankey diagrams"""

from typing import Optional, Dict, Any


class Edge:
    """Represents an edge (link/flow) in a Sankey diagram"""
    
    def __init__(self, source: str, target: str, value: float,
                 color: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize an edge
        
        Args:
            source: Source node label
            target: Target node label
            value: Flow value/width
            color: Optional edge color
            metadata: Optional metadata dictionary
        """
        self.source = source
        self.target = target
        self.value = value
        self.color = color or "rgba(100, 150, 200, 0.4)"
        self.metadata = metadata or {}
        
    def __repr__(self):
        return f"Edge(source='{self.source}', target='{self.target}', value={self.value})"
    
    def to_dict(self):
        """Convert edge to dictionary"""
        return {
            'source': self.source,
            'target': self.target,
            'value': self.value,
            'color': self.color,
            'metadata': self.metadata
        }