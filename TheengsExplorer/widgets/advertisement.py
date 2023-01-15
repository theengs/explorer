from bleak.uuids import uuidstr_to_str
from bluetooth_numbers import company
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from textual.widget import Widget


class CompanyID(Widget):
    """Widget that shows company ID and name."""

    def __init__(self, cic: int, compliant: bool):
        """Initialize CompanyID widget."""
        super().__init__()
        self.cic = cic
        self.compliant = compliant

    def __rich__(self) -> Text:
        """Render CompanyID widget."""
        try:
            manufacturer_name = company[self.cic]
        except KeyError:
            manufacturer_name = "Unknown"

        if self.compliant:
            return Text.assemble(
                f"0x{self.cic:04x} (", (manufacturer_name, "green bold"), ")"
            )
        else:
            return Text(f"0x{self.cic:04x}")


class HexData(Widget):
    """Widget that shows hex data with its length."""

    def __init__(self, data: bytes):
        """Initialize HexData widget."""
        super().__init__()
        self.data = data

    def __rich__(self) -> Text:
        """Render HexData widget."""
        return Text.assemble(
            (f"0x{bytes(self.data).hex()}", "cyan bold"), f" ({len(self.data)} bytes)"
        )


class UUID(Widget):
    """Widget that shows a UUID with description and colors."""

    def __init__(self, uuid128: str):
        """Initialize UUID widget."""
        super().__init__()
        self.uuid128 = uuid128

    def __rich__(self) -> Text:
        """Render UUID widget."""
        # Colorize the 16-bit UUID part in a standardized 128-bit UUID.
        if self.uuid128.startswith("0000") and self.uuid128.endswith(
            "-0000-1000-8000-00805f9b34fb"
        ):
            colored_uuid = Text.assemble(
                "0000",
                (self.uuid128[4:8], "green bold"),
                "-0000-1000-8000-00805f9b34fb",
            )
        else:
            colored_uuid = self.uuid128

        return Text.assemble(colored_uuid, f" ({uuidstr_to_str(self.uuid128)})")


class Advertisement(Widget):
    """Widget that shows raw advertisement data."""

    def __init__(self, advertisement_data, cid_compliant):
        """Initialize Advertisement widget."""
        super().__init__()
        self.advertisement_data = advertisement_data
        self.cid_compliant = cid_compliant

    def __rich__(self) -> Text:
        """Render Advertisement widget."""
        table = Table(show_header=False, show_edge=False, padding=0)

        # Show local name
        if self.advertisement_data.local_name:
            table.add_row(
                Text.assemble(
                    "local name: ", (self.advertisement_data.local_name, "green bold")
                )
            )

        # Show service UUIDs with their description
        if self.advertisement_data.service_uuids:
            tree = Tree("service UUIDs:")
            for uuid in sorted(self.advertisement_data.service_uuids):
                tree.add(UUID(uuid))
            table.add_row(tree)

        # Show manufacturer data
        if self.advertisement_data.manufacturer_data:
            tree = Tree("manufacturer data:")
            for cic, data in self.advertisement_data.manufacturer_data.items():
                tree.add(
                    Text.assemble(
                        CompanyID(cic, self.cid_compliant).render(),
                        ": ",
                        HexData(data).render(),
                    )
                )
            table.add_row(tree)

        # Show service data
        if self.advertisement_data.service_data:
            tree = Tree("service data:")
            for uuid, data in self.advertisement_data.service_data.items():
                tree.add(
                    Text.assemble(UUID(uuid).render(), ": ", HexData(data).render())
                )
            table.add_row(tree)

        return table
