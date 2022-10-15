from datetime import datetime

from decoder import decode


class DeviceInfo:
    def __init__(self, device, advertisement_data):
        self.device = device
        self.advertisement_data = advertisement_data

        self.time = datetime.now()
        self.previous_time = self.time

        self.decoded = decode(self.advertisement_data)

    def update(self, device, advertisement_data):
        self.device = device
        self.advertisement_data = advertisement_data

        # Store previous time for advertisement interval guessing
        self.previous_time = self.time
        self.time = datetime.now()

        decoded = decode(advertisement_data)
        # If advertisement contains timestamp, add current system time
        if "time" in decoded:
            decoded["system_time"] = int(datetime.now().timestamp())

        # Merge decoded data, with new data overriding previous data
        if self.decoded:
            if decoded:
                self.decoded = {**self.decoded, **decoded}
        else:
            self.decoded = decoded
