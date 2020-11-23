from time import sleep
import json
from model.model import state_getter
from gsr_fe import gsr_fe
from loguru import logger
from sqs_lib import receive_messages, delete_message
from svm.SVM import get_prediction
import numpy as np

WINDOW_SIZE = 10


def unpack_message(msg):
    return json.loads(msg.body)


def run():
    max_msg_count = 1  # number of messages to pull from queue at a time
    db = state_getter()
    while True:
        # read messages from the sqs queue
        messages = receive_messages('scares', max_msg_count, 1)
        if len(messages) > 0:
            for msg in messages:
                body = unpack_message(msg)
                ts = body['ts']
                user_id = body['user_id']
                logger.info("Processing for user {} at time {}".format(user_id, ts))
                # get the raw gsr readings from postgres
                raw_data = db.get_gsr_values(user_id, ts)
                # extract features from raw data
                features = gsr_fe(raw_data)
                # compute prediction for the data
                prediction = get_prediction(np.array(features).reshape(1, -1))
                logger.info("Prediction for user {} at {} is {}".format(user_id, ts, prediction))
                #  write the result of classification to the database
                db.insert_state(user_id, ts, prediction)
                #  delete the message so we don't read it twice
                delete_message(msg)
        sleep(2)


def main():
    run()


if __name__ == '__main__':
    main()
