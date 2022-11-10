from utils.block_header import BlockHeader
import json


class Block:
    def __init__(self, header: BlockHeader, data: []):
        self.header = header
        self.data = data

    def as_json(self):
        return {
            "header": {
                "previous_block_hash": self.header.previous_block_hash,
                "nonce": self.header.nonce
            },
            "transactions": json.dumps(self.data)
        }