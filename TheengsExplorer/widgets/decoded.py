import json

from rich.table import Table
from rich.text import Text
from textual.widget import Widget
from TheengsDecoder import getProperties


class Property(Widget):
    """Widget that shows a device property."""

    def __init__(self, entry, value, device_properties):
        """Initialize Property widget."""
        super().__init__()
        self.entry = entry
        self.value = value
        self.device_properties = device_properties

    def render(self) -> Text:
        """Render Property widget."""
        if self.entry in self.device_properties:
            unit = self.device_properties[self.entry]["unit"]
            if unit not in ["int", "hex"]:  # Only show real units
                return Text.assemble(
                    f"{self.device_properties[self.entry]['name']}: ",
                    (f"{self.value} {unit}", "cyan bold"),
                )
            else:
                return Text.assemble(
                    f"{self.device_properties[self.entry]['name']}: ",
                    (str(self.value), "cyan bold"),
                )
        else:  # There's no human-readable name of the property
            return Text.assemble(f"{self.entry}: ", (str(self.value), "cyan bold"))


class Decoded(Widget):
    """Widget that shows decoded data of an advertisement."""

    def __init__(self, decoded):
        """Initialize Decoded widget."""
        super().__init__()
        self.decoded = decoded

    def render(self) -> Table:
        """Render Decoded widget."""
        table = Table(show_header=False, show_edge=False, padding=0)

        if self.decoded:
            # Remove tempf, as well as keys we already show in the Device widget
            decoded = self.decoded.copy()  # Make local copy before popping
            for key in ["name", "brand", "model", "model_id", "tempf"]:
                try:
                    decoded.pop(key)
                except KeyError:
                    pass

            device_properties = json.loads(getProperties(self.decoded["model_id"]))[
                "properties"
            ]

            for entry in decoded:
                table.add_row(Property(entry, decoded[entry], device_properties))

        return table
