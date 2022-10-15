from textual.widget import Widget


class RSSI(Widget):
    """Widget that shows RSSI of a device."""

    def __init__(self, rssi: int):
        """Initialize RSSI widget."""
        super().__init__()
        self.rssi = rssi

    def render(self) -> str:
        """Render RSSI widget."""
        if self.rssi is not None:
            return f"{self.rssi} dBm"
        else:
            return ""
