from rich.table import Table
from rich.text import Text
from textual.widget import Widget


class Device(Widget):
    """Widget that shows device name, type and address."""

    def __init__(self, name, address, decoded):
        """Initialize Device widget."""
        super().__init__()
        self.name = name
        self.address = address
        self.decoded = decoded

    def render(self) -> Table:
        """Render Device widget."""
        table = Table(show_header=False, show_edge=False, padding=0)
        if self.name:
            table.add_row(Text(self.name, style="green bold"))

        table.add_row(self.address)

        if self.decoded:
            table.add_row(
                Text(
                    f"{self.decoded['brand']} {self.decoded['model']} ({self.decoded['model_id']})",
                    style="green bold",
                )
            )

        return table
