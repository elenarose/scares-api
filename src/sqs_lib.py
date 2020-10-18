import boto3
from botocore.exceptions import ClientError
sqs = boto3.resource('sqs')

#Code pulled from AWS Documentation

def get_queue(name):
    """
    Gets an SQS queue by name.
    :param name: The name that was used to create the queue.
    :return: A Queue object.
    """
    try:
        queue = sqs.get_queue_by_name(QueueName=name)
    except ClientError as error:
        raise error
    else:
        return queue

def send_message(queue_name, message_body, message_attributes=None):
    """
    Send a message to an Amazon SQS queue.

    :param queue_name: The queue name that receives the message.
    :param message_body: The body text of the message.
    :param message_attributes: Custom attributes of the message. These are key-value
                               pairs that can be whatever you want.
    :return: The response from SQS that contains the assigned message ID.
    """
    if not message_attributes:
        message_attributes = {}

    queue = get_queue(queue_name)

    try:
        response = queue.send_message(
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )
    except ClientError as error:
        raise error
    else:
        return response

def receive_messages(queue_name, max_number, wait_time):
    """
    Receive a batch of messages in a single request from an SQS queue.

    :param queue_name: The name of the queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    queue = get_queue(queue_name)
    try:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time
        )
        for msg in messages:
            print("Received message: %s: %s", msg.message_id, msg.body)
    except ClientError as error:
        print("Couldn't receive messages from queue: %s", queue)
        raise error
    else:
        return messages