"""Comprehensive demonstration of the interactive Sankey library"""

import pandas as pd
import numpy as np
import sys
sys.path.insert(0, 'src')

from sankey_interactive import SankeyDiagram


def create_sample_timeseries_data():
    """Create sample time series data for energy flows"""
    np.random.seed(42)
    
    dates = pd.date_range('2024-01', periods=12, freq='M')
    data = []
    
    sources = ['Solar', 'Wind', 'Coal', 'Nuclear', 'Gas']
    intermediates = ['Grid', 'Storage', 'Direct']
    targets = ['Residential', 'Commercial', 'Industrial']
    
    for date in dates:
        # Simulate seasonal variations
        month = date.month
        solar_factor = 1 + 0.3 * np.sin(2 * np.pi * month / 12)
        wind_factor = 1 + 0.2 * np.cos(2 * np.pi * month / 12)
        
        # Create flows
        for source in sources:
            for intermediate in intermediates:
                if source == 'Solar':
                    base_value = 100 * solar_factor
                elif source == 'Wind':
                    base_value = 80 * wind_factor
                else:
                    base_value = np.random.randint(50, 150)
                
                value = base_value * np.random.uniform(0.8, 1.2)
                
                data.append({
                    'date': date,
                    'source': source,
                    'target': intermediate,
                    'value': value,
                    'type': 'generation'
                })
        
        for intermediate in intermediates:
            for target in targets:
                value = np.random.uniform(50, 200)
                data.append({
                    'date': date,
                    'source': intermediate,
                    'target': target,
                    'value': value,
                    'type': 'distribution'
                })
    
    return pd.DataFrame(data)


def demo_basic_sankey():
    """Demo 1: Basic Sankey diagram"""
    print("=" * 60)
    print("DEMO 1: Basic Sankey Diagram")
    print("=" * 60)
    
    # Simple data
    data = pd.DataFrame({
        'source': ['A', 'A', 'B', 'B', 'C'],
        'target': ['D', 'E', 'D', 'E', 'E'],
        'value': [10, 20, 15, 5, 25]
    })
    
    diagram = SankeyDiagram(data)
    fig = diagram.render('source', 'target', 'value', 
                         title="Basic Sankey Diagram")
    fig.write_html('/tmp/demo1_basic.html')
    print("✓ Created basic Sankey diagram")
    print("  Saved to: /tmp/demo1_basic.html\n")


def demo_timeseries_sankey():
    """Demo 2: Time series Sankey with animation"""
    print("=" * 60)
    print("DEMO 2: Time Series Animation")
    print("=" * 60)
    
    data = create_sample_timeseries_data()
    
    # Filter to only show generation flows
    generation_data = data[data['type'] == 'generation'].copy()
    
    diagram = SankeyDiagram(generation_data, time_column='date')
    fig = diagram.render('source', 'target', 'value',
                         title="Energy Generation Over Time (Click Play!)",
                         show_timeline=True)
    
    fig.write_html('/tmp/demo2_timeseries.html')
    print("✓ Created time series Sankey with animation")
    print("  Saved to: /tmp/demo2_timeseries.html")
    print("  Features: Play/Pause button, Timeline slider\n")


def demo_histogram_edges():
    """Demo 3: Sankey with histogram-style edge coloring"""
    print("=" * 60)
    print("DEMO 3: Histogram Edge Coloring")
    print("=" * 60)
    
    data = create_sample_timeseries_data()
    
    # Use first month only
    first_month = data['date'].min()
    monthly_data = data[data['date'] == first_month].copy()
    
    diagram = SankeyDiagram(monthly_data)
    fig = diagram.render('source', 'target', 'value',
                         title="Energy Flows with Value-Based Coloring",
                         show_histogram=True,
                         show_timeline=False)
    
    fig.write_html('/tmp/demo3_histogram.html')
    print("✓ Created Sankey with histogram edge coloring")
    print("  Saved to: /tmp/demo3_histogram.html")
    print("  Features: Edges colored by value (blue=low, red=high)\n")


def demo_filters():
    """Demo 4: Interactive filters"""
    print("=" * 60)
    print("DEMO 4: Filtered Sankey Diagram")
    print("=" * 60)
    
    data = create_sample_timeseries_data()
    
    diagram = SankeyDiagram(data, time_column='date')
    
    # Add filter to show only high-value flows
    diagram.add_filter('high_value', lambda df: df[df['value'] > 100])
    
    # Add filter to show only renewable sources
    diagram.add_filter('renewable', 
                      lambda df: df[df['source'].isin(['Solar', 'Wind'])])
    
    fig = diagram.render('source', 'target', 'value',
                         title="Filtered: High-Value Renewable Flows Only",
                         show_timeline=True)
    
    fig.write_html('/tmp/demo4_filters.html')
    print("✓ Created filtered Sankey diagram")
    print("  Saved to: /tmp/demo4_filters.html")
    print("  Filters applied: value > 100, renewable sources only\n")


def demo_custom_metrics():
    """Demo 5: Custom node and edge metrics"""
    print("=" * 60)
    print("DEMO 5: Custom Metrics")
    print("=" * 60)
    
    data = create_sample_timeseries_data()
    first_month = data[data['date'] == data['date'].min()].copy()
    
    diagram = SankeyDiagram(first_month)
    
    # Custom node metric: total flow through each node
    def node_metric(df):
        sources = df.groupby('source')['value'].sum().to_dict()
        targets = df.groupby('target')['value'].sum().to_dict()
        return {**sources, **targets}
    
    # Custom edge metric: flow variance
    def edge_metric(df):
        return df.groupby(['source', 'target'])['value'].std().to_dict()
    
    diagram.set_node_metric(node_metric)
    diagram.set_edge_metric(edge_metric)
    
    fig = diagram.render('source', 'target', 'value',
                         title="Sankey with Custom Metrics",
                         show_histogram=True)
    
    fig.write_html('/tmp/demo5_metrics.html')
    print("✓ Created Sankey with custom metrics")
    print("  Saved to: /tmp/demo5_metrics.html")
    print("  Metrics: Node sizes by total flow, edge colors by variance\n")


def demo_complex_combined():
    """Demo 6: Everything combined"""
    print("=" * 60)
    print("DEMO 6: Full-Featured Interactive Dashboard")
    print("=" * 60)
    
    data = create_sample_timeseries_data()
    
    diagram = SankeyDiagram(data, time_column='date')
    
    # Add multiple filters
    diagram.add_filter('remove_small', lambda df: df[df['value'] > 50])
    
    # Custom metrics
    diagram.set_node_metric(
        lambda df: df.groupby('source')['value'].sum().to_dict()
    )
    
    fig = diagram.render('source', 'target', 'value',
                         title="Complete Interactive Energy Flow Dashboard",
                         show_histogram=True,
                         show_timeline=True)
    
    # Add annotations
    fig.add_annotation(
        text="Use the timeline slider to see changes over time<br>" +
             "Click Play to animate | Edges colored by flow value",
        xref="paper", yref="paper",
        x=0.5, y=-0.15,
        showarrow=False,
        font=dict(size=10, color="gray")
    )
    
    fig.write_html('/tmp/demo6_complete.html')
    print("✓ Created complete interactive dashboard")
    print("  Saved to: /tmp/demo6_complete.html")
    print("  Features: Timeline, Filters, Histogram coloring, Metrics\n")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 60)
    print("INTERACTIVE SANKEY LIBRARY - COMPREHENSIVE DEMONSTRATION")
    print("=" * 60 + "\n")
    
    # Run all demos
    demo_basic_sankey()
    demo_timeseries_sankey()
    demo_histogram_edges()
    demo_filters()
    demo_custom_metrics()
    demo_complex_combined()
    
    print("=" * 60)
    print("ALL DEMOS COMPLETE!")
    print("=" * 60)
    print("\nGenerated HTML files in /tmp/:")
    print("  1. demo1_basic.html        - Basic Sankey")
    print("  2. demo2_timeseries.html   - Animated timeline")
    print("  3. demo3_histogram.html    - Histogram coloring")
    print("  4. demo4_filters.html      - With filters applied")
    print("  5. demo5_metrics.html      - Custom metrics")
    print("  6. demo6_complete.html     - All features combined")
    print("\nOpen any file with: \"$BROWSER\" /tmp/demo*.html")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
