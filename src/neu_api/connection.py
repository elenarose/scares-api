import os
import json
import time

def connect(user_id):
    while True:

        URL_recieve = "http://localhost:20002/NeuLogAPI?GetSensorValue:[GSR],[{}]".format(user_id) # not going to be user id, but device id
        value = float(os.popen('curl' + '--fall --silent' + URL_recieve).read())
        value = json.loads(value)
	URL_send = "http://localhost:8080/data?\?user_id\={}\&value={}\&time={}".format(user_id, value['GetSensorData'][0], value['GetSenorData'][1])
	time.sleep(5)

if __name__ == '__main__':
	user_id = input("Enter a User ID: ")
	connect(user_id)
