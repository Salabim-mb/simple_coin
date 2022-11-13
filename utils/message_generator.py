import time
import base64
from utils.general.general import GeneralUtil
from multiprocessing import Process
import requests

from utils.node import Node


class MessageGenerator:
    """
    Class responsible for broadcasting test messages to known nodes
    """

    def __init__(self, node: Node):
        self.node = node
        generator_thread = Process(name="message_generator", target=self.__generate_messages)
        generator_thread.start()

    def __generate_messages(self) -> None:
        """
        [PRIVATE METHOD] 'Broadcast' test message by looping over node list
        :return:
        """
        while True:
            time.sleep(5)
            message, signature = GeneralUtil.generate_message_with_signature(self.node)
            for external_node in self.node.node_list:
                if external_node['name'] == self.node.name:
                    continue
                host = external_node['address']
                try:
                    requests.post(url=host + "/message", json={
                        'message': message,
                        'signature': signature
                    }, headers={
                        'X-Pub-Key': base64.b64encode(self.node.pub_key.to_string()),
                        'Origin': self.node.address
                    })
                except Exception as e:
                    print(f"Error with node {host}, couldn't find active target host. {str(e)}")
