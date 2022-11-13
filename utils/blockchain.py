from utils.block import Block
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
        # Fetch existing blocks by calling other nodes. If it's a first node, initialize blocks array with first block
        pass
