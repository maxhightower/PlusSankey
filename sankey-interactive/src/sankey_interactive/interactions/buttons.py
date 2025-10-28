class Buttons:
    def __init__(self):
        self.buttons = {}
    
    def add_button(self, name, action):
        """Add a button with a specified action."""
        self.buttons[name] = action
    
    def remove_button(self, name):
        """Remove a button by name."""
        if name in self.buttons:
            del self.buttons[name]
    
    def click_button(self, name):
        """Simulate a button click."""
        if name in self.buttons:
            action = self.buttons[name]
            action()  # Execute the associated action
        else:
            print(f"Button '{name}' not found.")
    
    def list_buttons(self):
        """List all available buttons."""
        return list(self.buttons.keys())