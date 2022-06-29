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

        # Merge decoded data, with new data overriding previous data
        decoded = decode(advertisement_data)
        if self.decoded:
            if decoded:
                self.decoded = {**self.decoded, **decoded}
        else:
            self.decoded = decoded
