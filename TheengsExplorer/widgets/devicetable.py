from deviceinfo import DeviceInfo
from rich.panel import Panel
from rich.table import Column, Table
from rich.text import Text
from textual.widget import Widget
from widgets.advertisement import Advertisement
from widgets.decoded import Decoded
from widgets.device import Device
from widgets.rssi import RSSI
from widgets.time import Time


class DeviceTable(Widget):
    def __init__(self):
        super().__init__()
        self.devices = {}

    def update_device(self, device, advertisement_data):
        """Add device if it doesn't exist yet; update it otherwise."""
        if device.address in self.devices:
            self.devices[device.address].update(device, advertisement_data)
        else:
            self.devices[device.address] = DeviceInfo(device, advertisement_data)

    def render(self):
        """Render device table."""
        table = Table(
            "Time",
            "Device",
            Column("RSSI", justify="right", max_width=8),
            "Decoded data",
            "Advertisement data",
            show_lines=True,
        )

        for info in self.devices.values():
            table.add_row(
                Time(info.time, info.previous_time),
                Device(
                    info.advertisement_data.local_name,
                    info.device.address,
                    info.decoded,
                ),
                RSSI(info.device.rssi),
                Decoded(info.decoded),
                Advertisement(info.advertisement_data),
            )
        if table.rows:
            return table
        else:
            return Panel(Text("Scanning for BLE devices...", justify="center"))
