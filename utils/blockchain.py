from utils.block import Block


class Blockchain:
    def __init__(self, node):
        self.node = node
        self.blocks: [Block] = []
        self.fetch_blocks()

    def fetch_blocks(self):
        # Fetch existing blocks by calling other nodes. If it's a first node, initialize blocks array with first block
        pass
