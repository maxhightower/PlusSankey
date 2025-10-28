class TimeSeries:
    def __init__(self, data):
        self.data = data
        self.current_time_index = 0

    def next_time_step(self):
        if self.current_time_index < len(self.data) - 1:
            self.current_time_index += 1
        return self.get_current_data()

    def previous_time_step(self):
        if self.current_time_index > 0:
            self.current_time_index -= 1
        return self.get_current_data()

    def get_current_data(self):
        return self.data[self.current_time_index]

    def filter_data(self, criteria):
        filtered_data = [entry for entry in self.data if self.meets_criteria(entry, criteria)]
        return filtered_data

    def meets_criteria(self, entry, criteria):
        # Implement criteria checking logic
        return True  # Placeholder for actual criteria checking

    def adjust_metrics(self, metric_function):
        for entry in self.data:
            entry['metric'] = metric_function(entry)
        return self.data

    def visualize(self):
        # Implement visualization logic
        pass  # Placeholder for actual visualization code