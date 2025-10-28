#!/usr/bin/env python3
"""
D3.js Sankey Renderer - Modern Web-Based Alternative to Plotly
=============================================================

This module provides a Python interface to generate D3.js-based Sankey diagrams.
It maintains the same API as the original Plotly-based implementation but renders
using D3.js for better performance and customization.
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import webbrowser
import tempfile
import os


class D3SankeyRenderer:
    """D3.js-based Sankey diagram renderer with Python API"""
    
    def __init__(self, data: pd.DataFrame, time_column: Optional[str] = None):
        """
        Initialize D3 Sankey renderer
        
        Args:
            data: DataFrame with flow data
            time_column: Optional time column for animations
        """
        self.data = data.copy()
        self.time_column = time_column
        self.filters = {}
        self.current_time_index = 0
        self.node_spacing_metric = None
        
        # Process time data if provided
        if time_column and time_column in data.columns:
            self.time_values = sorted(data[time_column].unique())
        else:
            self.time_values = []
    
    def add_filter(self, name: str, filter_func: Callable):
        """Add a data filter"""
        self.filters[name] = filter_func
    
    def set_node_spacing_metric(self, metric_func: Callable):
        """Set function to calculate horizontal node spacing"""
        self.node_spacing_metric = metric_func
    
    def apply_filters(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply all registered filters"""
        filtered_data = data.copy()
        for filter_func in self.filters.values():
            filtered_data = filter_func(filtered_data)
        return filtered_data
    
    def get_time_slice(self, time_index: int) -> pd.DataFrame:
        """Get data for specific time slice"""
        if not self.time_values or time_index >= len(self.time_values):
            return self.data
        
        time_value = self.time_values[time_index]
        return self.data[self.data[self.time_column] == time_value]
    
    def render(self, source_col: str, target_col: str, value_col: str,
               title: str = "Interactive Sankey Diagram",
               show_histogram: bool = False,
               show_timeline: bool = True,
               animation_duration: int = 800,
               transition_easing: str = "cubic-in-out",
               output_file: Optional[str] = None) -> str:
        """
        Render Sankey diagram using D3.js
        
        Args:
            source_col: Source column name
            target_col: Target column name  
            value_col: Value column name
            title: Diagram title
            show_histogram: Enable histogram-style edge coloring
            show_timeline: Show timeline controls for time series data
            animation_duration: Animation duration in milliseconds
            transition_easing: CSS easing function
            output_file: Optional output HTML file path
            
        Returns:
            Path to generated HTML file
        """
        
        # Prepare data for D3.js
        d3_data = self._prepare_d3_data(source_col, target_col, value_col, 
                                       show_histogram, show_timeline)
        
        # Generate HTML with embedded D3.js
        html_content = self._generate_html(
            d3_data, title, show_timeline, animation_duration, transition_easing
        )
        
        # Save to file
        if output_file is None:
            output_file = tempfile.mktemp(suffix='.html')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ D3.js Sankey diagram saved: {output_file}")
        return output_file
    
    def show(self, **kwargs) -> str:
        """Render and open in browser"""
        html_file = self.render(**kwargs)
        webbrowser.open(f'file://{os.path.abspath(html_file)}')
        return html_file
    
    def _prepare_d3_data(self, source_col: str, target_col: str, value_col: str,
                        show_histogram: bool, show_timeline: bool) -> Dict[str, Any]:
        """Prepare data structure for D3.js"""
        
        result = {
            'static': self._prepare_single_frame(self.data, source_col, target_col, value_col, show_histogram),
            'config': {
                'show_histogram': show_histogram,
                'show_timeline': show_timeline and bool(self.time_values),
                'source_col': source_col,
                'target_col': target_col,
                'value_col': value_col
            }
        }
        
        # Add time series data if available
        if show_timeline and self.time_values:
            result['timeseries'] = []
            for i, time_val in enumerate(self.time_values):
                time_data = self.get_time_slice(i)
                time_data = self.apply_filters(time_data)
                frame_data = self._prepare_single_frame(time_data, source_col, target_col, value_col, show_histogram)
                frame_data['time'] = str(time_val)
                frame_data['time_index'] = i
                result['timeseries'].append(frame_data)
        
        return result
    
    def _prepare_single_frame(self, data: pd.DataFrame, source_col: str, 
                             target_col: str, value_col: str, show_histogram: bool) -> Dict[str, Any]:
        """Prepare data for a single frame/time slice"""
        
        # Extract unique nodes
        all_nodes = list(set(data[source_col].tolist() + data[target_col].tolist()))
        node_dict = {node: idx for idx, node in enumerate(all_nodes)}
        
        # Prepare links
        links = []
        for _, row in data.iterrows():
            source_idx = node_dict[row[source_col]]
            target_idx = node_dict[row[target_col]]
            value = float(row[value_col])
            
            link = {
                'source': source_idx,
                'target': target_idx,
                'value': value,
                'source_name': row[source_col],
                'target_name': row[target_col]
            }
            
            # Add histogram coloring if enabled
            if show_histogram:
                link['color'] = self._get_histogram_color(value, data[value_col])
            
            links.append(link)
        
        # Prepare nodes
        nodes = []
        for node_name in all_nodes:
            # Calculate total flow through node
            inflow = data[data[target_col] == node_name][value_col].sum()
            outflow = data[data[source_col] == node_name][value_col].sum()
            total_flow = max(inflow, outflow)
            
            node_data = {
                'name': node_name,
                'id': node_dict[node_name],
                'total_flow': float(total_flow)
            }
            
            # Add custom spacing if metric is defined
            if self.node_spacing_metric:
                spacing_data = self.node_spacing_metric(data)
                if node_name in spacing_data:
                    node_data['spacing_metric'] = float(spacing_data[node_name])
            
            nodes.append(node_data)
        
        return {
            'nodes': nodes,
            'links': links,
            'node_count': len(nodes),
            'link_count': len(links)
        }
    
    def _get_histogram_color(self, value: float, all_values: pd.Series) -> str:
        """Generate histogram-style color based on value distribution"""
        # Normalize value to 0-1 range
        min_val, max_val = all_values.min(), all_values.max()
        if max_val == min_val:
            normalized = 0.5
        else:
            normalized = (value - min_val) / (max_val - min_val)
        
        # Convert to color (blue to red gradient)
        red = int(255 * normalized)
        blue = int(255 * (1 - normalized))
        return f"rgba({red}, 100, {blue}, 0.7)"
    
    def _generate_html(self, d3_data: Dict[str, Any], title: str, 
                      show_timeline: bool, animation_duration: int, 
                      transition_easing: str) -> str:
        """Generate complete HTML with D3.js Sankey implementation"""
        
        data_json = json.dumps(d3_data, indent=2)
        
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script src="https://unpkg.com/d3-sankey@0.12.3/dist/d3-sankey.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f8f9fa;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }}
        
        .title {{
            text-align: center;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #2c3e50;
        }}
        
        .controls {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        
        .timeline-control {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .timeline-slider {{
            width: 300px;
        }}
        
        .play-btn {{
            background: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
        }}
        
        .play-btn:hover {{
            background: #2980b9;
        }}
        
        .timeline-info {{
            font-size: 14px;
            color: #7f8c8d;
            min-width: 120px;
        }}
        
        .sankey-container {{
            text-align: center;
        }}
        
        .node {{
            fill: #3498db;
            stroke: #2c3e50;
            stroke-width: 1px;
            cursor: pointer;
        }}
        
        .node:hover {{
            fill: #e74c3c;
        }}
        
        .link {{
            fill: none;
            stroke-opacity: 0.6;
            cursor: pointer;
        }}
        
        .link:hover {{
            stroke-opacity: 0.8;
        }}
        
        .node-label {{
            font-size: 12px;
            font-weight: 500;
            fill: #2c3e50;
            text-anchor: middle;
            pointer-events: none;
        }}
        
        .tooltip {{
            position: absolute;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 12px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.2s;
        }}
        
        .stats {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            padding: 15px;
            background: #ecf0f1;
            border-radius: 6px;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #3498db;
        }}
        
        .stat-label {{
            font-size: 12px;
            color: #7f8c8d;
            text-transform: uppercase;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="title">{title}</div>
        
        {"<div class='controls' id='controls'></div>" if show_timeline else ""}
        
        <div class="sankey-container">
            <svg id="sankey"></svg>
        </div>
        
        <div class="stats" id="stats"></div>
    </div>
    
    <div class="tooltip" id="tooltip"></div>

    <script>
        // Data from Python
        const data = {data_json};
        
        // Configuration
        const CONFIG = {{
            width: 1000,
            height: 600,
            margin: {{ top: 20, right: 20, bottom: 20, left: 20 }},
            animationDuration: {animation_duration},
            transitionEasing: '{transition_easing}',
            showTimeline: {str(show_timeline).lower()}
        }};
        
        // Global state
        let currentTimeIndex = 0;
        let isPlaying = false;
        let playInterval = null;
        
        // Initialize the visualization
        class D3SankeyVisualization {{
            constructor() {{
                this.svg = d3.select("#sankey");
                this.tooltip = d3.select("#tooltip");
                this.setupSVG();
                this.setupControls();
                this.render(data.static);
                this.updateStats(data.static);
            }}
            
            setupSVG() {{
                this.svg
                    .attr("width", CONFIG.width)
                    .attr("height", CONFIG.height);
                    
                this.g = this.svg.append("g")
                    .attr("transform", `translate(${{CONFIG.margin.left}},${{CONFIG.margin.top}})`);
            }}
            
            setupControls() {{
                if (!CONFIG.showTimeline || !data.timeseries) return;
                
                const controls = d3.select("#controls");
                
                // Play/Pause button
                const playBtn = controls.append("button")
                    .attr("class", "play-btn")
                    .text("▶ Play")
                    .on("click", () => this.togglePlay());
                
                // Timeline slider
                const timelineDiv = controls.append("div")
                    .attr("class", "timeline-control");
                
                timelineDiv.append("span").text("Time:");
                
                const slider = timelineDiv.append("input")
                    .attr("type", "range")
                    .attr("class", "timeline-slider")
                    .attr("min", 0)
                    .attr("max", data.timeseries.length - 1)
                    .attr("value", 0)
                    .on("input", (event) => {{
                        currentTimeIndex = +event.target.value;
                        this.updateVisualization();
                    }});
                
                // Time info
                this.timeInfo = controls.append("div")
                    .attr("class", "timeline-info");
                
                this.updateTimeInfo();
            }}
            
            render(frameData) {{
                const innerWidth = CONFIG.width - CONFIG.margin.left - CONFIG.margin.right;
                const innerHeight = CONFIG.height - CONFIG.margin.top - CONFIG.margin.bottom;
                
                // Create Sankey generator
                const sankey = d3.sankey()
                    .nodeWidth(20)
                    .nodePadding(10)
                    .extent([[1, 1], [innerWidth - 1, innerHeight - 6]]);
                
                // Process data
                const sankeyData = sankey({{
                    nodes: frameData.nodes.map(d => ({{...d}})),
                    links: frameData.links.map(d => ({{...d}}))
                }});
                
                // Apply custom node spacing if available
                if (frameData.nodes.some(n => n.spacing_metric !== undefined)) {{
                    this.applyCustomSpacing(sankeyData, innerWidth);
                }}
                
                // Clear previous render
                this.g.selectAll("*").remove();
                
                // Render links
                this.g.append("g")
                    .selectAll("path")
                    .data(sankeyData.links)
                    .join("path")
                    .attr("class", "link")
                    .attr("d", d3.sankeyLinkHorizontal())
                    .attr("stroke", d => d.color || "#bdc3c7")
                    .attr("stroke-width", d => Math.max(1, d.width))
                    .on("mouseover", (event, d) => this.showTooltip(event, d, "link"))
                    .on("mouseout", () => this.hideTooltip());
                
                // Render nodes
                this.g.append("g")
                    .selectAll("rect")
                    .data(sankeyData.nodes)
                    .join("rect")
                    .attr("class", "node")
                    .attr("x", d => d.x0)
                    .attr("y", d => d.y0)
                    .attr("height", d => d.y1 - d.y0)
                    .attr("width", d => d.x1 - d.x0)
                    .on("mouseover", (event, d) => this.showTooltip(event, d, "node"))
                    .on("mouseout", () => this.hideTooltip());
                
                // Render node labels
                this.g.append("g")
                    .selectAll("text")
                    .data(sankeyData.nodes)
                    .join("text")
                    .attr("class", "node-label")
                    .attr("x", d => d.x0 < innerWidth / 2 ? d.x1 + 6 : d.x0 - 6)
                    .attr("y", d => (d.y1 + d.y0) / 2)
                    .attr("dy", "0.35em")
                    .attr("text-anchor", d => d.x0 < innerWidth / 2 ? "start" : "end")
                    .text(d => d.name);
            }}
            
            applyCustomSpacing(sankeyData, innerWidth) {{
                // Apply horizontal spacing based on custom metrics
                const levels = d3.group(sankeyData.nodes, d => d.x0);
                const sortedLevels = Array.from(levels.keys()).sort((a, b) => a - b);
                
                let currentX = 0;
                sortedLevels.forEach((levelX, levelIndex) => {{
                    const nodesAtLevel = levels.get(levelX);
                    const maxSpacing = d3.max(nodesAtLevel, d => d.spacing_metric || 0);
                    
                    // Update node positions
                    nodesAtLevel.forEach(node => {{
                        const nodeWidth = node.x1 - node.x0;
                        node.x0 = currentX;
                        node.x1 = currentX + nodeWidth;
                    }});
                    
                    // Calculate spacing to next level based on max metric
                    const baseSpacing = innerWidth / (sortedLevels.length + 1);
                    const metricSpacing = maxSpacing ? (maxSpacing / 50) * baseSpacing : 0;
                    currentX += baseSpacing + metricSpacing;
                }});
            }}
            
            updateVisualization() {{
                if (!data.timeseries || currentTimeIndex >= data.timeseries.length) return;
                
                const frameData = data.timeseries[currentTimeIndex];
                this.render(frameData);
                this.updateStats(frameData);
                this.updateTimeInfo();
            }}
            
            updateStats(frameData) {{
                const stats = d3.select("#stats");
                stats.selectAll("*").remove();
                
                const totalFlow = d3.sum(frameData.links, d => d.value);
                const nodeCount = frameData.nodes.length;
                const linkCount = frameData.links.length;
                
                [
                    {{ label: "Total Flow", value: totalFlow.toFixed(0) }},
                    {{ label: "Nodes", value: nodeCount }},
                    {{ label: "Links", value: linkCount }}
                ].forEach(stat => {{
                    const div = stats.append("div").attr("class", "stat");
                    div.append("div").attr("class", "stat-value").text(stat.value);
                    div.append("div").attr("class", "stat-label").text(stat.label);
                }});
            }}
            
            updateTimeInfo() {{
                if (!this.timeInfo || !data.timeseries) return;
                
                const current = data.timeseries[currentTimeIndex];
                this.timeInfo.text(`Time: ${{current.time}} (${{currentTimeIndex + 1}}/${{data.timeseries.length}})`);
            }}
            
            togglePlay() {{
                if (isPlaying) {{
                    this.stopPlay();
                }} else {{
                    this.startPlay();
                }}
            }}
            
            startPlay() {{
                isPlaying = true;
                d3.select(".play-btn").text("⏸ Pause");
                
                playInterval = setInterval(() => {{
                    currentTimeIndex = (currentTimeIndex + 1) % data.timeseries.length;
                    d3.select(".timeline-slider").property("value", currentTimeIndex);
                    this.updateVisualization();
                }}, CONFIG.animationDuration + 200);
            }}
            
            stopPlay() {{
                isPlaying = false;
                d3.select(".play-btn").text("▶ Play");
                if (playInterval) {{
                    clearInterval(playInterval);
                    playInterval = null;
                }}
            }}
            
            showTooltip(event, d, type) {{
                let content = "";
                if (type === "node") {{
                    content = `<strong>${{d.name}}</strong><br>Total Flow: ${{d.total_flow.toFixed(1)}}`;
                }} else {{
                    content = `<strong>${{d.source_name}} → ${{d.target_name}}</strong><br>Value: ${{d.value.toFixed(1)}}`;
                }}
                
                this.tooltip
                    .style("opacity", 1)
                    .html(content)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 10) + "px");
            }}
            
            hideTooltip() {{
                this.tooltip.style("opacity", 0);
            }}
        }}
        
        // Initialize visualization when page loads
        document.addEventListener('DOMContentLoaded', () => {{
            new D3SankeyVisualization();
        }});
    </script>
</body>
</html>
        """
        
        return html_template


# Compatibility class that maintains the original API
class SankeyDiagram(D3SankeyRenderer):
    """
    Drop-in replacement for the original Plotly-based SankeyDiagram
    
    This maintains the same API but uses D3.js for rendering instead of Plotly.
    """
    
    def __init__(self, data: pd.DataFrame, time_column: Optional[str] = None):
        super().__init__(data, time_column)
        self.fig = None  # For compatibility with existing code
    
    def render(self, source_col: str, target_col: str, value_col: str, **kwargs):
        """Render with same API as original, returns self for method chaining"""
        self.last_render_file = super().render(source_col, target_col, value_col, **kwargs)
        return self
    
    def show(self):
        """Show the rendered diagram in browser"""
        if hasattr(self, 'last_render_file'):
            webbrowser.open(f'file://{os.path.abspath(self.last_render_file)}')
        return self


def demo_d3_sankey():
    """Demonstrate D3.js Sankey capabilities"""
    
    print("🎨 D3.js Sankey Renderer Demo")
    print("=" * 40)
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range('2024-01', periods=4, freq='M')
    
    data = []
    for date in dates:
        flows = [
            {'source': 'Solar', 'target': 'Battery', 'value': np.random.uniform(80, 120)},
            {'source': 'Wind', 'target': 'Battery', 'value': np.random.uniform(60, 100)},
            {'source': 'Battery', 'target': 'Grid', 'value': np.random.uniform(100, 180)},
            {'source': 'Grid', 'target': 'Homes', 'value': np.random.uniform(80, 120)},
            {'source': 'Grid', 'target': 'Industry', 'value': np.random.uniform(60, 100)},
        ]
        
        for flow in flows:
            flow['date'] = date
            data.append(flow)
    
    df = pd.DataFrame(data)
    
    # Demo 1: Static D3.js Sankey
    print("\n1️⃣ Static D3.js Sankey...")
    static_data = df[df['date'] == df['date'].iloc[0]]
    renderer = D3SankeyRenderer(static_data)
    static_file = renderer.render('source', 'target', 'value', 
                                title='D3.js Static Sankey Demo',
                                show_timeline=False,
                                output_file='/tmp/d3_static_sankey.html')
    
    # Demo 2: Animated D3.js Sankey with timeline
    print("\n2️⃣ Animated D3.js Sankey...")
    animated_renderer = D3SankeyRenderer(df, time_column='date')
    animated_file = animated_renderer.render('source', 'target', 'value',
                                           title='D3.js Animated Sankey Demo',
                                           show_timeline=True,
                                           animation_duration=1000,
                                           output_file='/tmp/d3_animated_sankey.html')
    
    # Demo 3: With filters and histogram coloring
    print("\n3️⃣ D3.js with Filters and Histogram...")
    filtered_renderer = D3SankeyRenderer(df, time_column='date')
    filtered_renderer.add_filter('high_value', lambda d: d[d['value'] > 90])
    
    filtered_file = filtered_renderer.render('source', 'target', 'value',
                                           title='D3.js Filtered + Histogram Demo',
                                           show_histogram=True,
                                           show_timeline=True,
                                           output_file='/tmp/d3_filtered_sankey.html')
    
    # Demo 4: Drop-in replacement for existing code
    print("\n4️⃣ Drop-in Replacement Demo...")
    diagram = SankeyDiagram(df, time_column='date')
    diagram.add_filter('renewable', lambda d: d[d['source'].isin(['Solar', 'Wind'])])
    diagram.render('source', 'target', 'value',
                  title='Drop-in Replacement Demo',
                  show_timeline=True).show()
    
    print(f"\n✅ Demo complete! Generated files:")
    print(f"   📄 Static: {static_file}")
    print(f"   🎬 Animated: {animated_file}")
    print(f"   🎨 Filtered: {filtered_file}")
    print(f"\n🌐 Opening animated demo in browser...")
    
    return animated_file


if __name__ == "__main__":
    demo_d3_sankey()