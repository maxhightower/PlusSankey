import unittest
from sankey_interactive.interactions.filters import Filters
from sankey_interactive.interactions.buttons import Buttons
from sankey_interactive.interactions.controls import Controls

class TestInteractions(unittest.TestCase):

    def setUp(self):
        self.filters = Filters()
        self.buttons = Buttons()
        self.controls = Controls()

    def test_filter_nodes(self):
        # Assuming we have a method to add nodes and a method to filter them
        self.filters.add_node("Node1")
        self.filters.add_node("Node2")
        self.filters.apply_filter("Node1")
        self.assertIn("Node1", self.filters.filtered_nodes)
        self.assertNotIn("Node2", self.filters.filtered_nodes)

    def test_button_click(self):
        # Assuming we have a method to simulate button clicks
        self.buttons.add_button("TestButton")
        self.buttons.click("TestButton")
        self.assertTrue(self.buttons.is_clicked("TestButton"))

    def test_control_functionality(self):
        # Assuming we have methods to enable and disable controls
        self.controls.enable_control("Zoom")
        self.assertTrue(self.controls.is_enabled("Zoom"))
        self.controls.disable_control("Zoom")
        self.assertFalse(self.controls.is_enabled("Zoom"))

if __name__ == '__main__':
    unittest.main()