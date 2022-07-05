from deviceinfo import DeviceInfo
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.widget import Widget
from widgets.advertisement import Advertisement
from widgets.decoded import Decoded
from widgets.device import Device
from widgets.rssi import RSSI
from widgets.time import Time


class DeviceTable(Widget):
    def __init__(self, config, *args, **kwargs):
        self.config = config
        self.devices = {}
        super().__init__(*args, **kwargs)

    def update_device(self, device, advertisement_data):
        """Add device if it doesn't exist yet; update it otherwise."""
        if device.address in self.devices:
            self.devices[device.address].update(device, advertisement_data)
        else:
            self.devices[device.address] = DeviceInfo(device, advertisement_data)

    def render(self):
        """Render device table."""
        table = Table(show_lines=True)
        table.add_column("Time")
        table.add_column("Device")
        table.add_column("RSSI", justify="right", max_width=8)
        table.add_column("Decoded data")
        if self.config["advertisement"]:
            table.add_column("Advertisement data")

        for info in self.devices.values():
            cells = [
                Time(info.time, info.previous_time),
                Device(
                    info.advertisement_data.local_name,
                    info.device.address,
                    info.decoded,
                ),
                RSSI(info.device.rssi),
                Decoded(info.decoded),
            ]
            if self.config["advertisement"]:
                cells.append(Advertisement(info.advertisement_data))

            table.add_row(*cells)
        if table.rows:
            return table
        else:
            return Panel(Text("Scanning for BLE devices...", justify="center"))
