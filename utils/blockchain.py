import requests

from utils.block import Block
from utils.block_header import BlockHeader


class Blockchain:
    """
    Network representation of arranged nodes connected to mine and transfer cryptocurrency
    """

    def __init__(self):
        self.blocks: [Block] = []

    def fetch_blocks(self, node):
        """
        Fetch existing blocks by calling other nodes. If it's a first node, initialize blocks array with first block
        :return:
        """
        if len(node.node_list) == 0:
            header = BlockHeader()
            self.blocks = [Block(header, [])]
        else:
            for external_node in node.node_list:
                if external_node['address'] is node.address:
                    continue
                data = requests.get(url=external_node["address"] + "/get-blockchain")
                self.node.blockchain = data.json()
                break
