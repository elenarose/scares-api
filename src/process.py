from time import sleep
import json
from model.model import state_getter
from gsr_fe import gsr_fe
from loguru import logger
from sqs_lib import receive_messages
from svm.SVM import get_prediction
import numpy as np
WINDOW_SIZE = 10

def unpack_message(msg):
    return json.loads(msg.body)

def run():
    i = 0
    max_msg_count = 1 #number of messages to pull from queue at a time
    while i < 1:
        #read messages from the sqs queue
        messages = receive_messages('scares', max_msg_count, 2)
        if len(messages) > 0:
            for msg in messages:
                body = unpack_message(msg)
                ts = body['ts']
                user_id = body['user_id']
                logger.info("Processing for user {} at time {}".format(user_id, ts))
                raw_data = state_getter().get_gsr_values(user_id, '2020-11-17 22:22:41+02')  # 2020-11-17 22:22:41+02
                logger.info(raw_data)
                features = gsr_fe(raw_data)
                logger.info(features)
                prediction = get_prediction(np.array(features).reshape(1, -1))
                logger.info(prediction)
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