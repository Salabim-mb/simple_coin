import time
import base64
from utils.general.general import GeneralUtil
from multiprocessing import Process
import requests


def generate_messages(node) -> None:
    """
    [PRIVATE METHOD] 'Broadcast' test message by looping over node list
    :return:
    """
    print("Messenger daemon start")
    while True:
        time.sleep(5)
        message, signature = GeneralUtil.generate_message_with_signature(node)
        for external_node in node.node_list:
            if external_node['name'] == node.name:
                continue
            host = external_node['address']
            try:
                requests.post(url=host + "/message", json={
                    'message': message,
                    'signature': signature
                }, headers={
                    'X-Pub-Key': base64.b64encode(node.pub_key.to_string()),
                    'Origin': node.address
                })
            except Exception as e:
                print(f"Error with node {host}, couldn't find active target host. {str(e)}")


class MessageGenerator:
    """
    Class responsible for broadcasting test messages to known nodes
    """

    def __init__(self):
        pass

    def run(self, node):
        generator_thread = Process(name="message_generator", target=generate_messages, args=(node,))
        generator_thread.start()