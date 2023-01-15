from datetime import timedelta

from rich.table import Table
from rich.text import Text
from textual.widget import Widget


class Time(Widget):
    """Widget that shows time of last received advertisement and detected
    advertisement interval."""

    def __init__(self, time, previous_time):
        """Initialize Time widget."""
        super().__init__()
        self.time = time
        self.previous_time = previous_time

    def __rich__(self) -> Table:
        """Render Time widget."""
        table = Table(show_header=False, show_edge=False, padding=0)
        table.add_row(self.time.strftime("%H:%M:%S.%f"))

        advertisement_interval = (self.time - self.previous_time) / timedelta(
            milliseconds=1
        )
        if advertisement_interval > 0:
            table.add_row(
                Text.assemble("↔ ", (f"{advertisement_interval} ms", "cyan bold"))
            )

        return table
