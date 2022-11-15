import time
import datetime
import base64
from multiprocessing import Queue

from utils.general.general import GeneralUtil
from multiprocessing import Process
import requests


def generate_messages(q: Queue, node) -> None:
    """
    'Broadcast' test message by looping over node list
    :return:
    """
    print("Messenger daemon start")
    while True:
        time.sleep(1)
        message, signature = GeneralUtil.generate_message_with_signature(node)
        for external_node in node.node_list:
            if external_node['name'] == node.name:
                continue
            host = external_node['address']
            try:
                data = {
                    'message': message,
                    'signature': signature,
                    'timestamp': str(datetime.datetime.now().isoformat())
                }
                requests.post(url=host + "/message", json=data, headers={
                    'X-Pub-Key': base64.b64encode(node.pub_key.to_string()),
                    'Origin': node.address
                })
                q.put(data)
            except Exception as e:
                print(f"Error with node {host}, couldn't find active target host. {str(e)}")


class MessageGenerator:
    """
    Class responsible for broadcasting test messages to known nodes
    """

    def __init__(self):
        self.queue = None
        self.generator_thread = None

    def run(self, node):
        self.queue = Queue()
        self.generator_thread = Process(name="message_generator", target=generate_messages, args=(self.queue, node,))
        self.generator_thread.start()
