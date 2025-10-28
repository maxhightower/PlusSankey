import unittest
from sankey_interactive.visualization.renderer import Renderer
from sankey_interactive.visualization.time_series import TimeSeries
from sankey_interactive.visualization.histogram import Histogram

class TestVisualization(unittest.TestCase):

    def setUp(self):
        self.renderer = Renderer()
        self.time_series = TimeSeries()
        self.histogram = Histogram()

    def test_renderer_initialization(self):
        self.assertIsNotNone(self.renderer)
        self.assertIsInstance(self.renderer, Renderer)

    def test_time_series_initialization(self):
        self.assertIsNotNone(self.time_series)
        self.assertIsInstance(self.time_series, TimeSeries)

    def test_histogram_initialization(self):
        self.assertIsNotNone(self.histogram)
        self.assertIsInstance(self.histogram, Histogram)

    def test_render_diagram(self):
        result = self.renderer.render()
        self.assertTrue(result)

    def test_time_series_visualization(self):
        data = [1, 2, 3, 4, 5]
        self.time_series.load_data(data)
        result = self.time_series.visualize()
        self.assertTrue(result)

    def test_histogram_edge_behavior(self):
        edges = [1, 2, 3]
        self.histogram.load_edges(edges)
        result = self.histogram.apply_behavior()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()