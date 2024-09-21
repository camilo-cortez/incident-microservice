import os
import boto3
import logging
import requests

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def ensure_envvars():
    """Ensure that these environment variables are provided at runtime"""
    required_envvars = [
        "AWS_REGION",
        "SQSCONSUMER_QUEUENAME",
        "URL_BASE_INCIDENTS"
    ]

    missing_envvars = []
    for required_envvar in required_envvars:
        if not os.environ.get(required_envvar, ''):
            missing_envvars.append(required_envvar)

    if missing_envvars:
        message = "Required environment variables are missing: " + \
            repr(missing_envvars)
        raise AssertionError(message)


def process_message(message_body, message_attributes):
    logger.info(f"Processing message: {message_body}")
    response : object
    url: str
    if message_attributes is not None:
        event : str = message_attributes.get('event').get('StringValue')
        url_origin = message_attributes.get('url_origin').get('StringValue')
        method : str = message_attributes.get('method').get('StringValue')
    # Call incident api
    if event.lower() == 'incidents':
        url = os.environ["URL_BASE_INCIDENTS"]
    payload = {message_body}

    if method.lower() == 'post':
        response = requests.post(url, payload)
    elif method.lower() == 'delete':
        response = requests.delete(url, payload)
    elif method.lower() == 'put':
        response = requests.put(url, payload)
    else:
        response = requests.get(url, payload)

    print(f"Response: {response.text}, status: {response.status_code}")
    return response


def main():
    logger.info("SQS Consumer starting ...")
    try:
        ensure_envvars()
    except AssertionError as e:
        logger.error(str(e))
        raise

    queue_name = os.environ["SQSCONSUMER_QUEUENAME"]
    logger.info(f"Subscribing to queue {queue_name}")
    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    while True:
        messages = queue.receive_messages(
            MaxNumberOfMessages=1,
            WaitTimeSeconds=1,
            MessageAttributeNames=['All']
        )
        for message in messages:
            try:
                process_message(message.body, message.message_attributes)
            except Exception as e:
                print(f"Exception while processing message: {repr(e)}")
                continue

            message.delete()


if __name__ == "__main__":
    main()
