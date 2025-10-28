# Sankey Interactive

Sankey Interactive is a Python library designed for generating complex, interactive Sankey diagrams. This library provides a range of features for visualizing time series data, adjusting metrics for node sizes and edge distributions, and implementing interactive controls for enhanced user experience.

## Features

- **Complex Sankey Diagrams**: Create intricate diagrams that represent flows between nodes.
- **Time Series Visualization**: Visualize data over time with the ability to navigate through different time periods.
- **Adjustable Metrics**: Customize node sizes and edge distributions based on user-defined metrics.
- **Interactive Filters**: Filter nodes and edges dynamically based on user input.
- **Button Controls**: Manage interactions with buttons for a more intuitive user experience.
- **Histogram-like Edge Behavior**: Modify edge behavior to resemble histogram plots for better data representation.

## Installation

To install the Sankey Interactive library, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd sankey-interactive
pip install -r requirements.txt
```

## Usage

Here’s a simple example of how to create a basic Sankey diagram:

```python
from sankey_interactive import Diagram

# Create a new diagram
diagram = Diagram()

# Add nodes and edges
diagram.add_node("Node A", size=10)
diagram.add_node("Node B", size=20)
diagram.add_edge("Node A", "Node B", width=5)

# Render the diagram
diagram.render()
```

## Documentation

For detailed documentation, please refer to the [docs](docs/index.md).

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.