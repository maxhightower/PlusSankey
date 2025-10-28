"""Core Sankey Diagram class with timeline and metric support"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Callable, Any
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class SankeyDiagram:
    """Main class for creating interactive Sankey diagrams"""
    
    def __init__(self, data: pd.DataFrame, time_column: Optional[str] = None):
        """
        Initialize a Sankey diagram
        
        Args:
            data: DataFrame containing flow data
            time_column: Column name for time series data
        """
        self.data = data
        self.time_column = time_column
        self.current_time_index = 0
        self.node_metric = None
        self.edge_metric = None
        self.filters = {}
        self.fig = None
        
    def set_node_metric(self, metric_func: Callable[[pd.DataFrame], Dict[str, float]]):
        """Set function to calculate node sizes"""
        self.node_metric = metric_func
        
    def set_edge_metric(self, metric_func: Callable[[pd.DataFrame], Dict[tuple, float]]):
        """Set function to calculate edge widths"""
        self.edge_metric = metric_func
        
    def add_filter(self, name: str, filter_func: Callable[[pd.DataFrame], pd.DataFrame]):
        """Add a filter function"""
        self.filters[name] = filter_func
        
    def apply_filters(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply all registered filters"""
        filtered = data.copy()
        for filter_func in self.filters.values():
            filtered = filter_func(filtered)
        return filtered
    
    def get_time_slice(self, time_index: int) -> pd.DataFrame:
        """Get data for a specific time index"""
        if self.time_column is None:
            return self.data
        
        unique_times = sorted(self.data[self.time_column].unique())
        if time_index >= len(unique_times):
            time_index = len(unique_times) - 1
        
        selected_time = unique_times[time_index]
        return self.data[self.data[self.time_column] == selected_time]
    
    def create_sankey_data(self, data: pd.DataFrame, 
                          source_col: str, 
                          target_col: str, 
                          value_col: str,
                          show_histogram: bool = False) -> Dict[str, Any]:
        """Create Plotly Sankey data structure"""
        
        # Get unique nodes
        sources = data[source_col].unique()
        targets = data[target_col].unique()
        all_nodes = list(set(list(sources) + list(targets)))
        node_dict = {node: idx for idx, node in enumerate(all_nodes)}
        
        # Map source and target to indices
        source_indices = data[source_col].map(node_dict).tolist()
        target_indices = data[target_col].map(node_dict).tolist()
        values = data[value_col].tolist()
        
        # Calculate node values if metric is set
        node_values = None
        if self.node_metric:
            node_values = self.node_metric(data)
        
        # Customize edge colors for histogram effect
        edge_colors = self._calculate_edge_colors(data, source_col, target_col, 
                                                   value_col, show_histogram)
        
        return {
            'nodes': all_nodes,
            'source': source_indices,
            'target': target_indices,
            'value': values,
            'node_values': node_values,
            'edge_colors': edge_colors
        }
    
    def _calculate_edge_colors(self, data: pd.DataFrame, source_col: str, 
                               target_col: str, value_col: str, 
                               show_histogram: bool) -> List[str]:
        """Calculate edge colors based on histogram distribution"""
        if not show_histogram:
            return ['rgba(100, 150, 200, 0.4)'] * len(data)
        
        # Create color gradient based on value distribution
        values = data[value_col].values
        normalized = (values - values.min()) / (values.max() - values.min() + 1e-10)
        
        colors = []
        for val in normalized:
            # Color gradient from blue to red
            r = int(255 * val)
            b = int(255 * (1 - val))
            colors.append(f'rgba({r}, 100, {b}, 0.5)')
        
        return colors
    
    def render(self, source_col: str, target_col: str, value_col: str,
              title: str = "Interactive Sankey Diagram",
              show_histogram: bool = False,
              show_timeline: bool = True,
              animation_duration: int = 800,
              transition_easing: str = "cubic-in-out") -> go.Figure:
        """
        Render the interactive Sankey diagram
        
        Args:
            source_col: Column name for source nodes
            target_col: Column name for target nodes
            value_col: Column name for flow values
            title: Diagram title
            show_histogram: Show histogram coloring on edges
            show_timeline: Show timeline slider for time series data
            animation_duration: Duration of transitions in milliseconds (default 800)
                               Lower = faster, Higher = slower/smoother
                               Recommended: 300-2000
            transition_easing: Easing function for transitions. Options:
                              'linear', 'quad', 'cubic', 'sin', 'exp', 'circle',
                              'elastic', 'back', 'bounce', 'cubic-in-out' (default)
        """
        
        # Get current time slice
        current_data = self.get_time_slice(self.current_time_index)
        current_data = self.apply_filters(current_data)
        
        # Create Sankey data
        sankey_data = self.create_sankey_data(
            current_data, source_col, target_col, value_col, show_histogram
        )
        
        # Create figure
        if show_timeline and self.time_column:
            self.fig = self._create_timeline_figure(
                sankey_data, source_col, target_col, value_col, 
                title, show_histogram, animation_duration, transition_easing
            )
        else:
            self.fig = self._create_static_figure(sankey_data, title)
        
        return self.fig
    
    def _create_static_figure(self, sankey_data: Dict[str, Any], 
                             title: str) -> go.Figure:
        """Create a static Sankey figure"""
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=sankey_data['nodes'],
                color="rgba(100, 150, 200, 0.8)"
            ),
            link=dict(
                source=sankey_data['source'],
                target=sankey_data['target'],
                value=sankey_data['value'],
                color=sankey_data['edge_colors']
            )
        )])
        
        fig.update_layout(
            title_text=title,
            font_size=12,
            height=600
        )
        
        return fig
    
    def _create_timeline_figure(self, sankey_data: Dict[str, Any],
                               source_col: str, target_col: str, 
                               value_col: str, title: str,
                               show_histogram: bool,
                               animation_duration: int = 800,
                               transition_easing: str = "cubic-in-out") -> go.Figure:
        """Create Sankey figure with timeline controls"""
        
        unique_times = sorted(self.data[self.time_column].unique())
        
        # Create frames for animation
        frames = []
        for i, time in enumerate(unique_times):
            time_data = self.data[self.data[self.time_column] == time]
            time_data = self.apply_filters(time_data)
            
            frame_sankey = self.create_sankey_data(
                time_data, source_col, target_col, value_col, show_histogram
            )
            
            frames.append(go.Frame(
                data=[go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=frame_sankey['nodes'],
                        color="rgba(100, 150, 200, 0.8)"
                    ),
                    link=dict(
                        source=frame_sankey['source'],
                        target=frame_sankey['target'],
                        value=frame_sankey['value'],
                        color=frame_sankey['edge_colors']
                    )
                )],
                name=str(time)
            ))
        
        # Create figure with initial frame
        fig = go.Figure(
            data=frames[0].data,
            frames=frames
        )
        
        # Add slider
        sliders = [{
            'active': 0,
            'yanchor': 'top',
            'y': 0,
            'xanchor': 'left',
            'x': 0.1,
            'currentvalue': {
                'prefix': f'{self.time_column}: ',
                'visible': True,
                'xanchor': 'right'
            },
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'steps': [
                {
                    'args': [[f.name], {
                        'frame': {
                            'duration': animation_duration, 
                            'redraw': True
                        },
                        'mode': 'immediate',
                        'transition': {
                            'duration': animation_duration,
                            'easing': transition_easing
                        }
                    }],
                    'label': str(time),
                    'method': 'animate'
                }
                for f, time in zip(frames, unique_times)
            ]
        }]
        
        # Add play/pause buttons
        updatemenus = [{
            'buttons': [
                {
                    'args': [None, {
                        'frame': {
                            'duration': animation_duration, 
                            'redraw': True
                        },
                        'fromcurrent': True,
                        'transition': {
                            'duration': animation_duration,
                            'easing': transition_easing
                        }
                    }],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True},
                                     'mode': 'immediate'}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]
        
        fig.update_layout(
            title_text=title,
            font_size=12,
            height=700,
            sliders=sliders,
            updatemenus=updatemenus
        )
        
        return fig
    
    def show(self):
        """Display the diagram"""
        if self.fig:
            self.fig.show()
