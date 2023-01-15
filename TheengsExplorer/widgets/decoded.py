from datetime import datetime
import json

import humanize
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

    def __rich__(self) -> Text:
        """Render Property widget."""
        if self.entry in self.device_properties:
            unit = self.device_properties[self.entry]["unit"]
            if unit in ["int", "hex", "string", "status"]:  # Don't show these units
                return Text.assemble(
                    f"{self.device_properties[self.entry]['name']}: ",
                    (str(self.value), "cyan bold"),
                )
            else:
                return Text.assemble(
                    f"{self.device_properties[self.entry]['name']}: ",
                    (f"{self.value} {unit}", "cyan bold"),
                )
        else:  # There's no human-readable name of the property
            return Text.assemble(f"{self.entry}: ", (str(self.value), "cyan bold"))


class Decoded(Widget):
    """Widget that shows decoded data of an advertisement."""

    def __init__(self, decoded, temperature_unit):
        """Initialize Decoded widget."""
        super().__init__()
        self.decoded = decoded
        if temperature_unit == "celsius":
            self.hidden_temperature_unit = "tempf"
        else:
            self.hidden_temperature_unit = "tempc"

    def __rich__(self) -> Table:
        """Render Decoded widget."""
        table = Table(show_header=False, show_edge=False, padding=0)

        if self.decoded:
            decoded = self.decoded.copy()  # Make local copy before deleting keys and changing values

            # Make timestamps human-readable
            if "system_time" in decoded:
                timedelta = int(datetime.now().timestamp()) - decoded["system_time"]
                for key in decoded.keys():
                    if key.startswith("time_"):
                        decoded[key] = humanize.naturaltime(decoded["time"] - decoded[key] + timedelta)

            # Remove keys we already show in the Device or Advertisement widgets,
            # as well as tempf or tempc according to the user's chosen temperature unit.
            for key in ["name", "brand", "model", "model_id", "cidc", "time", "system_time", self.hidden_temperature_unit]:
                try:
                    del decoded[key]
                except KeyError:
                    pass
            # Remove tempf_* or tempc_* keys
            for key in list(decoded.keys()):
                if key.startswith(f"{self.hidden_temperature_unit}_"):
                    del decoded[key]

            device_properties = json.loads(getProperties(self.decoded["model_id"]))[
                "properties"
            ]

            # Change tempc device properties to tempf if using Fahrenheit
            if self.hidden_temperature_unit == "tempc":
                for key in list(device_properties.keys()):
                    if key.startswith("tempc"):
                        device_properties[key]["unit"] = "°F"
                        device_properties[key.replace("tempc", "tempf")] = device_properties.pop(key)

            for entry in decoded:
                table.add_row(Property(entry, decoded[entry], device_properties))

        return table
