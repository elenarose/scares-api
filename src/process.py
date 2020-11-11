from sqs_lib import receive_messages
from time import sleep
import json
from model.model import state_getter
from loguru import logger
WINDOW_SIZE = 10

def unpack_message(msg):
    return json.loads(msg.body)

def run():
    i = 0
    max_msg_count = 1 #number of messages to pull from queue at a time
    while i < 1:
        #read messages from the sqs queue
        #messages = receive_messages('scares', max_msg_count, 2)
        #if len(messages) > 0:
            #for msg in messages:
        #body = unpack_message(msg)
        #print(body['user_id'], body['ts'])
        ts = "2020-10-19 10:27:59+02"
        raw_data = state_getter.get_gsr_values(2, ts - WINDOW_SIZE, ts)
        logger.info(raw_data)
        #TODO do math with raw_data
        # feature extraction and classification happens here for a segment of data


        #TODO
        # write the result of classification to the database

        #TODO
        # delete the message so we don't read it twice
        sleep(2)
        i = i + 1

def main():
    run()

if __name__ == '__main__':
    main()