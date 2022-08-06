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

from bleak import BleakScanner
from textual.app import App
from textual.widgets import Footer, ScrollView
from widgets.devicetable import DeviceTable


class TheengsExplorerApp(App):
    """Textual app that shows BLE advertisements."""

    def __init__(self, config, *args, **kwargs):
        self.config = config
        if config["adapter"]:
            self.scanner = BleakScanner(adapter=config["adapter"], scanning_mode=config["scanning_mode"])
        else:
            self.scanner = BleakScanner(scanning_mode=config["scanning_mode"])
        self.scanner.register_detection_callback(self.detection_callback)
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

    config = {"adapter": None, "advertisement": True, "scanning_mode": "active"}

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
        help="Scanning mode",
    )
    args = parser.parse_args()

    if args.adapter:
        config["adapter"] = args.adapter
    config["scanning_mode"] = args.scanning_mode

    TheengsExplorerApp.run(config=config, title="Theengs Explorer")
