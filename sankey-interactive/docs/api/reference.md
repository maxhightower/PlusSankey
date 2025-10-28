# API Reference for Sankey Interactive Library

## Overview

The Sankey Interactive library provides a powerful tool for generating complex, interactive Sankey diagrams. This document serves as a reference for the various classes and methods available in the library.

## Classes

### Diagram

- **Description**: Manages the overall structure of the Sankey diagram.
- **Methods**:
  - `add_node(node)`: Adds a node to the diagram.
  - `add_edge(edge)`: Adds an edge between two nodes.
  - `render()`: Renders the diagram based on the current nodes and edges.

### Node

- **Description**: Represents a node in the Sankey diagram.
- **Properties**:
  - `size`: The size of the node, adjustable based on metrics.
- **Methods**:
  - `update_metrics()`: Updates the metrics for the node.

### Edge

- **Description**: Represents an edge in the Sankey diagram.
- **Properties**:
  - `width`: The width of the edge, adjustable based on distribution.
- **Methods**:
  - `update_metrics()`: Updates the metrics for the edge.

### Renderer

- **Description**: Responsible for rendering the Sankey diagram.
- **Methods**:
  - `draw()`: Draws the current state of the diagram.
  - `update()`: Updates the visual representation based on user interactions.

### TimeSeries

- **Description**: Handles time series data visualization.
- **Methods**:
  - `navigate(time)`: Navigates through the time series data.

### Histogram

- **Description**: Modifies edge behavior to act like histogram plots.
- **Methods**:
  - `apply_histogram_behavior()`: Applies histogram-like behavior to edges.

### Filters

- **Description**: Provides methods for filtering nodes and edges.
- **Methods**:
  - `filter_nodes(criteria)`: Filters nodes based on specified criteria.
  - `filter_edges(criteria)`: Filters edges based on specified criteria.

### Buttons

- **Description**: Manages button interactions for the Sankey diagram.
- **Methods**:
  - `add_button(label, action)`: Adds a button with a specified action.

### Controls

- **Description**: Provides methods for controlling the diagram's interactive features.
- **Methods**:
  - `enable_interaction()`: Enables user interaction with the diagram.
  - `disable_interaction()`: Disables user interaction with the diagram.

### NodeMetrics

- **Description**: Functions and classes for calculating and adjusting node metrics.
- **Methods**:
  - `calculate_size(data)`: Calculates the size of a node based on input data.

### EdgeMetrics

- **Description**: Functions and classes for calculating and adjusting edge metrics.
- **Methods**:
  - `calculate_width(data)`: Calculates the width of an edge based on input data.

## Usage

To use the Sankey Interactive library, import the necessary classes and create instances as needed. For example:

```python
from sankey_interactive.core import Diagram, Node, Edge

diagram = Diagram()
node1 = Node(size=10)
node2 = Node(size=20)
edge = Edge(width=5)

diagram.add_node(node1)
diagram.add_node(node2)
diagram.add_edge(edge)
diagram.render()
```

## Conclusion

This API reference provides a comprehensive overview of the classes and methods available in the Sankey Interactive library. For further details, please refer to the individual class documentation and examples provided in the `examples` directory.