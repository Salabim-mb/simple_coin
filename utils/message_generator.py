import time
import base64
from utils.general.general import GeneralUtil
import threading
import requests

MINING_REWARD = 2


class MessageGenerator:
    def __init__(self, node):
        self.node = node
        generator_thread = threading.Thread(name="message_generator", target=self.generate_messages)
        generator_thread.start()

    def generate_messages(self):
        while True:
            time.sleep(10)
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
                    self.node.wallet.balance -= MINING_REWARD + self.node.wallet.tran_fee
                except Exception as e:
                    print(f"Error with node {host}, couldn't find active target host. {str(e)}")
