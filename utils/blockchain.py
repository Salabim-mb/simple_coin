import requests

from utils.block import Block
from utils.block_header import BlockHeader
from utils.node import Node


class Blockchain:
    """
    Network representation of arranged nodes connected to mine and transfer cryptocurrency
    """

    def __init__(self, node: Node):
        self.node = node
        self.blocks: [Block] = []
        self.fetch_blocks()

    def fetch_blocks(self):
        """
        Fetch existing blocks by calling other nodes. If it's a first node, initialize blocks array with first block
        :return:
        """
        if len(self.node.node_list) == 0:
            header = BlockHeader()
            self.blocks = [Block(header, [])]
        else:
            for external_node in self.node.node_list:
                data = requests.get(url=external_node["address"] + "/get-blockchain")
                self.node.blockchain = data.json()
