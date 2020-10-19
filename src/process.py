from sqs_lib import receive_messages
from time import sleep
from model.model import get_gsr_values

def unpack_message(msg):
    return msg.body

def run():
    i = 0
    max_msg_count = 1 #number of messages to pull from queue at a time
    while i < 100:
        #read messages from the sqs queue
        messages = receive_messages('new_data', max_msg_count, 2)
        if len(messages) > 0:
            for msg in messages:
                body = unpack_message(msg)
                raw_data = get_gsr_values(body.user_id, body.ts - 5, body.ts)
                #TODO do math with raw_data
                # feature extraction and classification happens here for a segment of data
                #TODO
                # write the result of classification to the database
        sleep(2)
        i = i + 1

def main():
    run()

if __name__ == '__main__':
    main()