import requests
import json
from config import vin, url, username, password
from numcompress import decompress


def send_to_api(input_stream):

    headers = {'Content-type': 'application/json'}

    send_list = decompress(input_stream[1])

    params = dict(vin=vin,
                  speed=int(send_list[0]),
                  ignition=int(send_list[1]),
                  fuel=int(send_list[2]),
                  errors_count=int(send_list[3]),
                  lat=send_list[4],
                  lon=send_list[5],
                  timestamp=input_stream[3])
    try:
        resp = requests.post(url=url, auth=(username, password), headers=headers, data=json.dumps(params))
    except:
        return False
    return resp.ok

