import boto3
from botocore.exceptions import ClientError
sqs = boto3.resource('sqs')

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