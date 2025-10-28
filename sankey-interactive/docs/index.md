# Sankey Interactive Library Documentation

## Overview

The Sankey Interactive library is designed for generating complex, interactive Sankey diagrams. It provides a range of features that allow users to visualize time series data, adjust metrics for node sizes and edge distributions, and apply various filters to enhance the interactivity of the diagrams.

## Features

- **Complex Sankey Diagrams**: Create detailed and informative Sankey diagrams that represent flow data effectively.
- **Time Series Visualization**: Visualize data over time with the TimeSeries class, allowing users to navigate through different time periods.
- **Adjustable Metrics**: Customize node sizes and edge distributions based on user-defined metrics for better representation of data.
- **Interactive Filters**: Use the Filters class to filter nodes and edges dynamically based on specific criteria.
- **Button Interactions**: Manage user interactions with buttons to control the display and behavior of the Sankey diagram.
- **Histogram-like Edge Behavior**: Modify edge behavior to resemble histogram plots for enhanced data representation.

## Installation

To install the Sankey Interactive library, you can use pip:

```bash
pip install sankey-interactive
```

## Quick Start

Here’s a simple example to get you started with creating a basic Sankey diagram:

```python
from sankey_interactive import Diagram

# Create a new Sankey diagram
diagram = Diagram()

# Add nodes and edges
diagram.add_node("Node 1", size=10)
diagram.add_node("Node 2", size=20)
diagram.add_edge("Node 1", "Node 2", width=5)

# Render the diagram
diagram.render()
```

## Documentation

For detailed documentation on each component of the library, please refer to the following sections:

- [API Reference](api/reference.md): Comprehensive details on classes and methods available in the library.
- [Examples](../examples): Practical examples demonstrating various features and functionalities of the library.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](../CONTRIBUTING.md) file for guidelines on how to contribute to the project.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for more details.