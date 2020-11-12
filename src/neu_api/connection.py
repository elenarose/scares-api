import json
import time
from datetime import datetime
import requests

def connect():
    while True:

        try:
            req = requests.get("http://{}:{}/NeuLogAPI?GetSensorValue:[GSR],[{}]".format(address, port, device_id))

        except ConnectionError:
            print("Not Connected to API...Trying Again...")
            continue

        value = json.loads(req.text)
        value = value['GetSensorValue'][0]

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        post_call = "curl http://localhost:8080/data?\?user_id\={}\&value={}\&time={}".format(device_id, value, current_time)

        time.sleep(5)

if __name__ == '__main__':

 device_id = input("Enter a User ID: ")
 address = input("Enter the address of API: ")
 port = input("Enter the port of the API: ")
 connect(device_id)
