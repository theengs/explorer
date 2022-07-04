import json
import struct

from TheengsDecoder import decodeBLE


def decode(advertisement_data):
    """Decode advertisement data with Theengs Decoder."""
    data_json = {}

    if advertisement_data.local_name:
        data_json["name"] = advertisement_data.local_name

    if advertisement_data.manufacturer_data:
        dstr = str(
            struct.pack(
                "<H", list(advertisement_data.manufacturer_data.keys())[0]
            ).hex()
        )
        dstr += str(list(advertisement_data.manufacturer_data.values())[0].hex())
        data_json["manufacturerdata"] = dstr

    if advertisement_data.service_data:
        # Try to decode advertisement with service data for each UUID separately.
        for uuid, data in advertisement_data.service_data.items():
            # TheengsDecoder only accepts 16 bit UUIDs, this converts the 128 bit UUID to 16 bit.
            data_json["servicedatauuid"] = uuid[4:8]
            data_json["servicedata"] = data.hex()
            try:
                # Return the first one that decodes correctly.
                return json.loads(decodeBLE(json.dumps(data_json)))
            except TypeError:
                pass  # Just try the following UUID if Theengs Decoder can't decode the data.

        # No UUID resulted in successful decoding.
        return {}

    if data_json:
        try:
            data_json = json.loads(decodeBLE(json.dumps(data_json)))
        except TypeError:  # Theengs Decoder can't decode the data.
            data_json = {}

    return data_json
