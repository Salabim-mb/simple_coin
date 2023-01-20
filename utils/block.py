from utils.block_header import BlockHeader
import json
from anytree import NodeMixin


class Block(NodeMixin):
    """
    Class for single block representation
    """
    def __init__(self, header: BlockHeader, data: [], parent):
        super(Block, self).__init__()
        self.header = header
        self.data = data
        self.parent = parent
        if header.previous_block_hash:
            self.name = "Prev. #: " + header.previous_block_hash[0:5]
        else:
            self.name = "First block"

    def as_json(self):
        """
        Get JSON representation of Block class
        :return: Block instances as JSON object
        """
        return {
            "header": {
                "previous_block_hash": self.header.previous_block_hash,
                "nonce": self.header.nonce
            },
            "transactions": json.dumps(self.data)
        }