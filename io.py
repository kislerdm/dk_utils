# Functions to operate files
# Author: D.Kisler <admin@dkisler.de>

import pickle
import json
from kafka import KafkaProducer


def save_object(obj, filename):
    """
    Function to save/pickle python object

    :param filename: path to file
    """

    with open(filename, 'wb') as output:  # Overwrites any existing file
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def read_object(filename):
    """
    Function to read/un-pickle python object

    :param filename: path to pickle file

    """

    with open(filename, 'rb') as input_stream:
        obj = pickle.load(input_stream)
    return obj


def msg_post_kafka(msg,
                   topic,
                   is_json=True,
                   host='localhost:9092',
                   key=None,
                   close=True
                   ):
    """
    Function to send msg to kafka under the topic

    :param msg: message to be send
    :param topic: kafka topic
    :param is_json: is msg json?
    :param host: host adress (and port) of a kafka server
    :param key: optional topic key
    :param close: shall the connection be closed
    """

    if is_json:
        producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                 bootstrap_servers=host)
        try:
            producer.send(topic, msg)
            if close:
                producer.close()
            return None, True
        except Exception as ex:
            if close:
                producer.close()
            return str(ex), False
    else:
        producer = KafkaProducer(bootstrap_servers=host)
        try:
            producer.send(topic=topic, key=key, value=msg)
            if close:
                producer.close()
            return None, True
        except Exception as ex:
            if close:
                producer.close()
            return str(ex), False
