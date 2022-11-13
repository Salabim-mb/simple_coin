from utils.block_header import BlockHeader
import json


class Block:
    """
    Node representation in blockchain
    """

    def __init__(self, header: BlockHeader, data: []):
        self.header = header
        self.data = data

    def as_json(self) -> {}:
        """
        Creates ready to jsonify object containing data for hash calculation
        :return: Described above object
        """
        return {
            "header": {
                "previous_block_hash": self.header.previous_block_hash,
                "nonce": self.header.nonce
            },
            "transactions": json.dumps(self.data)
        }