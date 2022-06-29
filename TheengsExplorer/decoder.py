import json
import struct

from TheengsDecoder import decodeBLE


def decode(advertisement_data):
    data_json = {}

    if advertisement_data.service_data:
        dstr = list(advertisement_data.service_data.keys())[0]
        # TheengsDecoder only accepts 16 bit UUIDs, this converts the 128 bit UUID to 16 bit.
        data_json["servicedatauuid"] = dstr[4:8]
        dstr = str(list(advertisement_data.service_data.values())[0].hex())
        data_json["servicedata"] = dstr

    if advertisement_data.manufacturer_data:
        dstr = str(
            struct.pack(
                "<H", list(advertisement_data.manufacturer_data.keys())[0]
            ).hex()
        )
        dstr += str(list(advertisement_data.manufacturer_data.values())[0].hex())
        data_json["manufacturerdata"] = dstr

    if advertisement_data.local_name:
        data_json["name"] = advertisement_data.local_name

    if data_json:
        try:
            data_json = json.loads(decodeBLE(json.dumps(data_json)))
        except TypeError:  # Theengs Decoder can't decode the data
            data_json = {}

    return data_json
