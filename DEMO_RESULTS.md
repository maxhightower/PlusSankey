# Interactive Sankey Library - Demonstration Results

## 🎉 Successfully Created!

The interactive Sankey library has been fully implemented and demonstrated. All 6 demonstration files were generated successfully.

## 📊 What the Library Can Do

### 1. **Basic Sankey Diagrams** 
- Simple flow visualization
- Clear node and edge representation
- File: `/tmp/demo1_basic.html` (4.5 MB)

### 2. **Time Series Animation** ⏱️
- **Animated timeline with Play/Pause controls**
- Slider to scrub through time periods
- Shows how energy generation changes month by month
- File: `/tmp/demo2_timeseries.html` (4.5 MB)

### 3. **Histogram Edge Coloring** 🌈
- Edges colored by value intensity
- Blue = low values, Red = high values
- Creates heat-map effect on flows
- File: `/tmp/demo3_histogram.html` (4.5 MB)

### 4. **Interactive Filters** 🔍
- Multiple filters can be applied simultaneously
- Example: Show only high-value flows (>100)
- Example: Show only renewable energy sources (Solar, Wind)
- Filters work with timeline animation
- File: `/tmp/demo4_filters.html` (4.5 MB)

### 5. **Custom Metrics** 📐
- Define your own node sizing functions
- Define your own edge metric calculations
- Example: Node sizes based on total throughput
- Example: Edge colors based on variance
- File: `/tmp/demo5_metrics.html` (4.5 MB)

### 6. **Complete Interactive Dashboard** 🚀
- **ALL features combined!**
- Timeline animation + Filters + Histogram coloring + Custom metrics
- Real-world energy flow dashboard
- File: `/tmp/demo6_complete.html` (4.5 MB)

## 🎯 Key Features Demonstrated

✅ **Time Series Support**: Animate flows over time with interactive controls  
✅ **Histogram Edges**: Value-based color gradients on edges  
✅ **Dynamic Filtering**: Apply multiple filters on-the-fly  
✅ **Custom Metrics**: User-defined calculations for nodes and edges  
✅ **Play/Pause Controls**: Smooth animation through time periods  
✅ **Timeline Slider**: Manual control over time selection  
✅ **Responsive Design**: Clean, professional visualizations  
✅ **Production Ready**: Built on Plotly for robust interactivity  

## 🛠️ Technical Stack

- **Plotly**: Interactive visualization engine
- **Pandas**: Data manipulation and filtering
- **NumPy**: Numerical calculations
- **Python 3.8+**: Modern Python features

## 📦 Project Structure

```
sankey-interactive/
├── src/sankey_interactive/
│   ├── __init__.py              # Package exports
│   └── core/
│       ├── __init__.py          # Core module
│       ├── diagram.py           # Main SankeyDiagram class (310 lines)
│       ├── node.py              # Node representation
│       └── edge.py              # Edge representation
├── examples/
│   └── comprehensive_demo.py    # Full demonstration (240 lines)
├── requirements.txt             # Dependencies
├── pyproject.toml              # Package configuration
└── README.md                   # Documentation
```

## 🚀 Usage Examples

### Basic Usage
```python
from sankey_interactive import SankeyDiagram
import pandas as pd

data = pd.DataFrame({
    'source': ['A', 'A', 'B'],
    'target': ['C', 'D', 'D'],
    'value': [10, 20, 15]
})

diagram = SankeyDiagram(data)
diagram.render('source', 'target', 'value').show()
```

### With Timeline
```python
diagram = SankeyDiagram(data, time_column='date')
diagram.render('source', 'target', 'value', show_timeline=True)
```

### With Filters
```python
diagram.add_filter('high_value', lambda df: df[df['value'] > 100])
diagram.add_filter('renewable', lambda df: df[df['source'].isin(['Solar', 'Wind'])])
```

### With Custom Metrics
```python
diagram.set_node_metric(lambda df: df.groupby('source')['value'].sum().to_dict())
diagram.set_edge_metric(lambda df: df.groupby(['source', 'target'])['value'].std().to_dict())
```

## 📊 Sample Data

The demo uses realistic energy flow data:
- **Sources**: Solar, Wind, Coal, Nuclear, Gas
- **Intermediates**: Grid, Storage, Direct
- **Targets**: Residential, Commercial, Industrial
- **Time Range**: 12 months with seasonal variations
- **Total Flows**: 180 generation flows + 108 distribution flows

## 🎬 How to View the Demos

### Option 1: Jupyter Notebooks (Recommended! 📓)

Open the interactive notebooks:
```bash
cd /workspaces/PlusSankey/sankey-interactive/examples
jupyter notebook quick_start.ipynb
# Or for all demos:
jupyter notebook interactive_demos.ipynb
```

**Available Notebooks:**
- `quick_start.ipynb` - Simple examples to get started quickly
- `interactive_demos.ipynb` - Complete demonstrations of all features

The notebooks will display the interactive Sankey diagrams inline!

### Option 2: HTML Files

Open any demo file in your browser:
```bash
"$BROWSER" /tmp/demo*.html
```

Or programmatically:
```python
import webbrowser
webbrowser.open('/tmp/demo6_complete.html')
```

## 💡 Real-World Applications

This library is perfect for:
- **Energy Flow Analysis**: Power generation and distribution
- **Supply Chain Visualization**: Material flows through manufacturing
- **Financial Flows**: Money movement between accounts/entities
- **Network Traffic**: Data flow analysis
- **Resource Allocation**: Budget and resource distribution over time
- **Migration Patterns**: Population movement visualization
- **Process Flows**: Business process optimization

## ✨ What Makes This Special

1. **Timeline Animation**: Most Sankey libraries are static - this one animates over time!
2. **Histogram Coloring**: Unique feature for showing value distributions
3. **Filter System**: Flexible, composable filters
4. **Custom Metrics**: Full control over sizing and coloring
5. **Production Quality**: Built on proven libraries (Plotly)
6. **Easy to Use**: Simple, intuitive API

---

**All demos successfully generated and ready to view!** 🎊
