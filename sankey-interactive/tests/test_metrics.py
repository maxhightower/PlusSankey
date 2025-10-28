import pytest
from sankey_interactive.metrics.node_metrics import calculate_node_metrics
from sankey_interactive.metrics.edge_metrics import calculate_edge_metrics

def test_calculate_node_metrics():
    # Test with sample data
    sample_data = {
        'node1': [10, 20, 30],
        'node2': [5, 15, 25]
    }
    expected_metrics = {
        'node1': {'average': 20, 'total': 60},
        'node2': {'average': 15, 'total': 45}
    }
    metrics = calculate_node_metrics(sample_data)
    assert metrics == expected_metrics

def test_calculate_edge_metrics():
    # Test with sample data
    sample_edges = {
        'edge1': [1, 2, 3],
        'edge2': [4, 5, 6]
    }
    expected_edge_metrics = {
        'edge1': {'width': 2, 'distribution': [1, 2, 3]},
        'edge2': {'width': 5, 'distribution': [4, 5, 6]}
    }
    edge_metrics = calculate_edge_metrics(sample_edges)
    assert edge_metrics == expected_edge_metrics

def test_empty_node_metrics():
    # Test with empty data
    sample_data = {}
    expected_metrics = {}
    metrics = calculate_node_metrics(sample_data)
    assert metrics == expected_metrics

def test_empty_edge_metrics():
    # Test with empty data
    sample_edges = {}
    expected_edge_metrics = {}
    edge_metrics = calculate_edge_metrics(sample_edges)
    assert edge_metrics == expected_edge_metrics