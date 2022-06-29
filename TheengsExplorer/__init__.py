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
import asyncio

from bleak import BleakScanner
from textual.app import App
from textual.widgets import ScrollView
from widgets.devicetable import DeviceTable


class TheengsExplorerApp(App):
    """Textual app that shows BLE advertisements."""

    async def detection_callback(self, device, advertisement_data) -> None:
        """Process detected advertisement data from device."""
        self.device_table.update_device(device, advertisement_data)
        await self.scroll_view.update(self.device_table.render(), home=False)

    async def ble_scan(self) -> None:
        """Register detection callback and start BLE scanner."""
        scanner = BleakScanner()
        scanner.register_detection_callback(self.detection_callback)
        await scanner.start()
        while True:
            await asyncio.sleep(5.0)

    async def on_load(self) -> None:
        """Bind keys when the app loads."""
        await self.bind("q", "quit", "Quit")
        await self.bind("escape", "quit", "Quit")

    async def on_mount(self) -> None:
        """Create ScrollView and start BLE scan."""
        self.device_table = DeviceTable()
        self.scroll_view = ScrollView(self.device_table)

        await self.view.dock(self.scroll_view, edge="top")

        asyncio.create_task(self.ble_scan())


if __name__ == "__main__":
    TheengsExplorerApp.run(title="Theengs Explorer")
