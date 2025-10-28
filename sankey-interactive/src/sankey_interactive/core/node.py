"""Node representation for Sankey diagrams"""

from typing import Optional, Dict, Any


class Node:
    """Represents a node in a Sankey diagram"""
    
    def __init__(self, label: str, value: Optional[float] = None, 
                 color: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize a node
        
        Args:
            label: Node label/name
            value: Optional node value/size
            color: Optional node color
            metadata: Optional metadata dictionary
        """
        self.label = label
        self.value = value
        self.color = color or "rgba(100, 150, 200, 0.8)"
        self.metadata = metadata or {}
        
    def __repr__(self):
        return f"Node(label='{self.label}', value={self.value})"
    
    def to_dict(self):
        """Convert node to dictionary"""
        return {
            'label': self.label,
            'value': self.value,
            'color': self.color,
            'metadata': self.metadata
        }