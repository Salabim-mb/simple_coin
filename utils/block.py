from block_header import BlockHeader


class Block:
    def __init__(self):
        self.header = BlockHeader()
        self.data = []