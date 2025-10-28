#!/usr/bin/env python3
"""
Alternative Sankey Renderers - Breaking Away from Plotly
========================================================

This demo shows several alternatives to Plotly for creating Sankey diagrams.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import seaborn as sns
from typing import Dict, List, Tuple
import json

# Sample data for demonstrations
sample_data = pd.DataFrame({
    'source': ['Raw Materials', 'Raw Materials', 'Raw Materials', 
               'Processing A', 'Processing A', 'Processing B', 
               'Assembly', 'Assembly', 'QA Check'],
    'target': ['Processing A', 'Processing B', 'Processing C',
               'Assembly', 'Quality Check', 'Assembly',
               'QA Check', 'Packaging', 'Shipping'],
    'value': [45, 30, 25, 40, 5, 28, 35, 33, 35]
})

class MatplotlibSankeyRenderer:
    """Custom Sankey renderer using Matplotlib"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.nodes = {}
        self.flows = []
        
    def render(self, source_col: str, target_col: str, value_col: str, 
               title: str = "Sankey Diagram", figsize: tuple = (14, 8)):
        """Render Sankey diagram using matplotlib"""
        
        # Extract unique nodes and assign positions
        all_nodes = list(set(self.data[source_col].tolist() + self.data[target_col].tolist()))
        self._calculate_node_positions(all_nodes, source_col, target_col)
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect('equal')
        
        # Draw flows first (so they appear behind nodes)
        self._draw_flows(ax, source_col, target_col, value_col)
        
        # Draw nodes
        self._draw_nodes(ax, value_col)
        
        # Styling
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        plt.tight_layout()
        
        return fig
    
    def _calculate_node_positions(self, all_nodes: List[str], source_col: str, target_col: str):
        """Calculate positions for nodes in a Sankey layout"""
        # Group nodes by their position in the flow (left to right)
        stages = {}
        
        # Start with source-only nodes (leftmost)
        sources = set(self.data[source_col].unique())
        targets = set(self.data[target_col].unique())
        
        # Leftmost: nodes that are sources but not targets
        stage_0 = sources - targets
        stages[0] = list(stage_0)
        
        # Middle stages: nodes that are both sources and targets
        middle_nodes = sources & targets
        
        # Rightmost: nodes that are targets but not sources  
        stage_final = targets - sources
        
        # Simple positioning: spread middle nodes across 2-3 stages
        if middle_nodes:
            mid_list = list(middle_nodes)
            stages[1] = mid_list[:len(mid_list)//2 + 1]
            if len(mid_list) > 1:
                stages[2] = mid_list[len(mid_list)//2 + 1:]
        
        stages[3] = list(stage_final)
        
        # Assign x,y coordinates
        for stage, nodes in stages.items():
            x = 1 + stage * 2.5  # Horizontal spacing
            for i, node in enumerate(nodes):
                y = 2 + i * (6 / max(len(nodes), 1))  # Vertical spacing
                self.nodes[node] = {'x': x, 'y': y, 'total_value': 0}
        
        # Calculate total values for node sizing
        for _, row in self.data.iterrows():
            source, target = row[source_col], row[target_col]
            value = row['value']
            self.nodes[source]['total_value'] += value
            self.nodes[target]['total_value'] += value
    
    def _draw_nodes(self, ax, value_col: str):
        """Draw nodes as rectangles"""
        for node_name, node_data in self.nodes.items():
            x, y = node_data['x'], node_data['y']
            total_value = node_data['total_value']
            
            # Node size based on total value
            width = 0.3
            height = max(0.5, total_value / 50)  # Scale height by value
            
            # Create rectangle
            rect = patches.Rectangle(
                (x - width/2, y - height/2), width, height,
                facecolor='lightblue', edgecolor='navy', linewidth=2,
                alpha=0.8
            )
            ax.add_patch(rect)
            
            # Add label
            ax.text(x, y, node_name, ha='center', va='center', 
                   fontsize=9, fontweight='bold', wrap=True)
    
    def _draw_flows(self, ax, source_col: str, target_col: str, value_col: str):
        """Draw curved flows between nodes"""
        # Color palette for flows
        colors = sns.color_palette("husl", len(self.data))
        
        for idx, (_, row) in enumerate(self.data.iterrows()):
            source = row[source_col]
            target = row[target_col]
            value = row[value_col]
            
            if source in self.nodes and target in self.nodes:
                self._draw_single_flow(ax, source, target, value, colors[idx])
    
    def _draw_single_flow(self, ax, source: str, target: str, value: float, color):
        """Draw a single curved flow between two nodes"""
        source_pos = self.nodes[source]
        target_pos = self.nodes[target]
        
        # Flow coordinates
        x1, y1 = source_pos['x'] + 0.15, source_pos['y']  # Right edge of source
        x2, y2 = target_pos['x'] - 0.15, target_pos['y']   # Left edge of target
        
        # Control points for Bezier curve
        ctrl_x = (x1 + x2) / 2
        ctrl1 = (ctrl_x, y1)
        ctrl2 = (ctrl_x, y2)
        
        # Create curved path
        verts = [(x1, y1), ctrl1, ctrl2, (x2, y2)]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        path = Path(verts, codes)
        
        # Flow width based on value
        line_width = max(2, value / 5)
        
        # Draw the flow
        patch = PathPatch(path, facecolor='none', edgecolor=color, 
                         linewidth=line_width, alpha=0.6)
        ax.add_patch(patch)
        
        # Add value label on flow
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y, f'{int(value)}', ha='center', va='center',
               fontsize=8, bbox=dict(boxstyle="round,pad=0.1", 
               facecolor='white', alpha=0.8))


class SVGSankeyRenderer:
    """Export Sankey as SVG for web embedding"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def render_svg(self, source_col: str, target_col: str, value_col: str,
                   title: str = "Sankey Diagram") -> str:
        """Generate SVG string for web embedding"""
        
        # Use matplotlib renderer to create the plot
        matplotlib_renderer = MatplotlibSankeyRenderer(self.data)
        fig = matplotlib_renderer.render(source_col, target_col, value_col, title)
        
        # Convert to SVG string
        import io
        svg_buffer = io.StringIO()
        fig.savefig(svg_buffer, format='svg', bbox_inches='tight')
        svg_string = svg_buffer.getvalue()
        plt.close(fig)
        
        return svg_string
    
    def save_html(self, filename: str, source_col: str, target_col: str, value_col: str):
        """Save as standalone HTML file"""
        svg_content = self.render_svg(source_col, target_col, value_col)
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sankey Diagram</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .sankey-container {{ text-align: center; }}
            </style>
        </head>
        <body>
            <div class="sankey-container">
                {svg_content}
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html_template)
        
        print(f"✅ Saved HTML file: {filename}")


class NetworkXSankeyRenderer:
    """Alternative using NetworkX for graph-based approach"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        
    def render_network(self, source_col: str, target_col: str, value_col: str):
        """Render as network graph (not true Sankey, but useful for analysis)"""
        try:
            import networkx as nx
        except ImportError:
            print("❌ NetworkX not installed. Install with: pip install networkx")
            return None
            
        # Create directed graph
        G = nx.DiGraph()
        
        # Add edges with weights
        for _, row in self.data.iterrows():
            G.add_edge(row[source_col], row[target_col], weight=row[value_col])
        
        # Create layout
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Position nodes
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Draw network
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=1000, alpha=0.8, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', ax=ax)
        
        # Draw edges with width based on weight
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        nx.draw_networkx_edges(G, pos, width=[w/10 for w in weights], 
                              alpha=0.7, edge_color='gray', arrows=True,
                              arrowsize=20, ax=ax)
        
        ax.set_title("Network View of Flow Data", fontsize=14)
        ax.axis('off')
        plt.tight_layout()
        
        return fig


def demo_all_alternatives():
    """Run demonstrations of all alternative renderers"""
    
    print("🎨 Alternative Sankey Renderers Demo")
    print("=" * 50)
    
    # 1. Matplotlib Custom Sankey
    print("\n1️⃣ Custom Matplotlib Sankey...")
    matplotlib_renderer = MatplotlibSankeyRenderer(sample_data)
    fig1 = matplotlib_renderer.render('source', 'target', 'value', 
                                     'Custom Matplotlib Sankey')
    fig1.savefig('/tmp/matplotlib_sankey.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("✅ Saved: /tmp/matplotlib_sankey.png")
    
    # 2. SVG Export for Web
    print("\n2️⃣ SVG Export for Web...")
    svg_renderer = SVGSankeyRenderer(sample_data)
    svg_renderer.save_html('/tmp/sankey_web.html', 'source', 'target', 'value')
    
    # 3. NetworkX Alternative
    print("\n3️⃣ NetworkX Graph View...")
    try:
        network_renderer = NetworkXSankeyRenderer(sample_data)
        fig3 = network_renderer.render_network('source', 'target', 'value')
        if fig3:
            fig3.savefig('/tmp/networkx_sankey.png', dpi=150, bbox_inches='tight')
            plt.show()
            print("✅ Saved: /tmp/networkx_sankey.png")
    except Exception as e:
        print(f"⚠️ NetworkX demo failed: {e}")
    
    print("\n🎉 Demo complete! Check /tmp/ for output files.")
    
    # Summary of approaches
    print("\n📋 Summary of Alternative Approaches:")
    print("━" * 50)
    print("1. Matplotlib Custom: Full control, publication quality")
    print("2. SVG Export: Web-friendly, scalable graphics") 
    print("3. NetworkX: Graph analysis, different perspective")
    print("4. D3.js Integration: Most interactive (not shown)")
    print("5. Bokeh/HoloViews: Dashboard-friendly (not shown)")


if __name__ == "__main__":
    demo_all_alternatives()