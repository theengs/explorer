"""
  TheengsExplorer - Decode things and devices and show data in a textual interface

    Copyright: (c) Koen VERVLOESEM

    This file is part of TheengsExplorer.

    TheengsExplorer is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    TheengsExplorer is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from argparse import ArgumentParser
import platform

from bleak import BleakScanner
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.scroll_view import ScrollView
from widgets.devicetable import DeviceTable

if platform.system() == "Linux":
    from bleak.assigned_numbers import AdvertisementDataType
    from bleak.backends.bluezdbus.advertisement_monitor import OrPattern
    from bleak.backends.bluezdbus.scanner import BlueZScannerArgs


class TheengsExplorerApp(App):
    """Textual app that shows BLE advertisements."""

    def __init__(self, config, *args, **kwargs):
        self.config = config

        scanner_kwargs = {"scanning_mode": config["scanning_mode"]}

        # Passive scanning with BlueZ needs at least one or_pattern.
        # The following matches all devices.
        if platform.system() == "Linux" and config["scanning_mode"] == "passive":
            scanner_kwargs["bluez"] = BlueZScannerArgs(
                or_patterns=[
                    OrPattern(0, AdvertisementDataType.FLAGS, b"\x06"),
                    OrPattern(0, AdvertisementDataType.FLAGS, b"\x1a"),
                ]
            )

        if config["adapter"]:
            scanner_kwargs["adapter"] = config["adapter"]

        scanner_kwargs["detection_callback"] = self.detection_callback

        self.scanner = BleakScanner(**scanner_kwargs)
        self.scanning = True
        super().__init__(*args, **kwargs)

    async def detection_callback(self, device, advertisement_data) -> None:
        """Process detected advertisement data from device."""

        self.query_one(DeviceTable).update_device(device, advertisement_data)
        if isinstance(self.focused, ScrollView):
            await self.focused.update(self.device_table.render(), home=False)

    def on_load(self) -> None:
        """Bind keys when the app loads."""
        self.bind("q", "quit", description="Quit")
        self.bind("s", "toggle_scan", description="Toggle scan")
        self.bind("a", "toggle_advertisement", description="Show advertisement")

    async def action_toggle_scan(self) -> None:
        """Start or stop BLE scanner."""
        if self.scanning:
            await self.scanner.stop()
            self.scanning = False
        else:
            await self.scanner.start()
            self.scanning = True

    async def action_toggle_advertisement(self) -> None:
        """Show or hide advertisement data."""
        if self.config["advertisement"]:
            self.config["advertisement"] = False
        else:
            self.config["advertisement"] = True

    def compose(self) -> ComposeResult:
        """Create app child widgets."""

        yield Header()
        yield ScrollView(DeviceTable(self.config));
        yield Footer()

    async def on_mount(self) -> None:
        """Create ScrollView and start BLE scan."""

        self.query_one(ScrollView).focus()
        await self.scanner.start()


if __name__ == "__main__":

    config = {"adapter": None, "advertisement": True, "scanning_mode": "active", "temperature_unit": "celsius"}

    parser = ArgumentParser()
    parser.add_argument(
        "-a",
        "--adapter",
        type=str,
        help="Bluetooth adapter (e.g. hci1 on Linux)",
    )
    parser.add_argument(
        "-s",
        "--scanning-mode",
        dest="scanning_mode",
        type=str,
        default="active",
        choices=("active", "passive"),
        help="Scanning mode (default: active)",
    )
    parser.add_argument(
        "-t",
        "--temperature-unit",
        dest="temperature_unit",
        type=str,
        default="celsius",
        choices=("celsius", "fahrenheit"),
        help="Temperature unit (default: celsius)",
    )

    args = parser.parse_args()

    if args.adapter:
        config["adapter"] = args.adapter
    config["scanning_mode"] = args.scanning_mode
    config["temperature_unit"] = args.temperature_unit

    # title="Theengs Explorer"
    if __name__ == "__main__":
        TheengsExplorerApp(config=config).run()
