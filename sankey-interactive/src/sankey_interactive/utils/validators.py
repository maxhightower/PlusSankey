def validate_node_data(node_data):
    if not isinstance(node_data, dict):
        raise ValueError("Node data must be a dictionary.")
    
    required_keys = ['id', 'size']
    for key in required_keys:
        if key not in node_data:
            raise ValueError(f"Missing required key: {key} in node data.")
    
    if not isinstance(node_data['id'], str):
        raise ValueError("Node ID must be a string.")
    
    if not isinstance(node_data['size'], (int, float)) or node_data['size'] < 0:
        raise ValueError("Node size must be a non-negative number.")

def validate_edge_data(edge_data):
    if not isinstance(edge_data, dict):
        raise ValueError("Edge data must be a dictionary.")
    
    required_keys = ['source', 'target', 'width']
    for key in required_keys:
        if key not in edge_data:
            raise ValueError(f"Missing required key: {key} in edge data.")
    
    if not isinstance(edge_data['source'], str) or not isinstance(edge_data['target'], str):
        raise ValueError("Source and target must be strings.")
    
    if not isinstance(edge_data['width'], (int, float)) or edge_data['width'] < 0:
        raise ValueError("Edge width must be a non-negative number.")

def validate_data_structure(data):
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary containing 'nodes' and 'edges'.")
    
    if 'nodes' not in data or 'edges' not in data:
        raise ValueError("Data must contain 'nodes' and 'edges' keys.")
    
    if not isinstance(data['nodes'], list) or not isinstance(data['edges'], list):
        raise ValueError("Nodes and edges must be lists.")
    
    for node in data['nodes']:
        validate_node_data(node)
    
    for edge in data['edges']:
        validate_edge_data(edge)