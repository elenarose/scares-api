import json
import time
from datetime import datetime
import requests
import os

def connect(device_id, neu_address, neu_port, user_id=1):

    aws_address = 'http://scares-api-dev.us-east-1.elasticbeanstalk.com/data'
    header = {'Authorization': 'E!&3F3ugu;Pvnc6E'}
    user_param = {"user_id":user_id}


    while True:

        timestamps = []
        gsr_values = []

        for i in range(5):

            try:
                req = requests.get("http://{}:{}/NeuLogAPI?GetSensorValue:[GSR],[{}]".format(neu_address, neu_port, device_id))

            except:
                print("Not Connected to API...Trying Again...")
                time.sleep(5)
                continue

            value = json.loads(req.text)
            value = value['GetSensorValue'][0]

            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S+02")

            timestamps.append(current_time)
            gsr_values.append(value)

            data_post = {"timestamps": timestamps, "gsr_values": gsr_values}

        requests.post(aws_address, json=data_post, headers=header, params=user_param)
        #time.sleep(5)

if __name__ == '__main__':

 device_id = input("Enter a device ID: ")
 address = input("Enter the address of API: ")
 port = input("Enter the port of the API: ")
 connect(device_id, address, port)
