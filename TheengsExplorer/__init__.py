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
from textual.app import App
from textual.widgets import Footer, ScrollView
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
        self.device_table.update_device(device, advertisement_data)
        await self.scroll_view.update(self.device_table.render(), home=False)

    async def on_load(self) -> None:
        """Bind keys when the app loads."""
        await self.bind("q", "quit", "Quit")
        await self.bind("s", "toggle_scan", "Toggle scan")
        await self.bind("a", "toggle_advertisement", "Show advertisement")

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

    async def on_mount(self) -> None:
        """Create ScrollView and start BLE scan."""
        self.device_table = DeviceTable(self.config)
        self.scroll_view = ScrollView(self.device_table)

        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.scroll_view, edge="top")

        await self.scanner.start()


if __name__ == "__main__":

    config = {"adapter": None, "advertisement": True, "scanning_mode": "active", "temp_unit": "celsius"}

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

    TheengsExplorerApp.run(config=config, title="Theengs Explorer")
