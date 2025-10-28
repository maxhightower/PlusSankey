# Example of a time series Sankey diagram visualization

import numpy as np
import matplotlib.pyplot as plt
from sankey_interactive.visualization.time_series import TimeSeries
from sankey_interactive.core.diagram import Diagram

def generate_time_series_data():
    # Generate some example time series data
    time_steps = np.arange(10)
    data = np.random.rand(10, 5)  # 10 time steps, 5 nodes
    return time_steps, data

def main():
    time_steps, data = generate_time_series_data()
    
    # Create a Sankey diagram instance
    diagram = Diagram()
    
    # Create a TimeSeries instance for visualization
    time_series_visualization = TimeSeries(diagram, time_steps, data)
    
    # Render the initial diagram
    time_series_visualization.render()
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()