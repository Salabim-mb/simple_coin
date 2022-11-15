from utils.block import Block
import requests

from utils.block_header import BlockHeader


class Blockchain:
    def __init__(self, node):
        self.node = node
        self.blocks: [Block] = []
        self.fetch_blocks()

    def fetch_blocks(self):
        if len(self.node.node_list) > 1:
            for external_node in self.node.node_list:
                if external_node['name'] == self.node.name:
                    continue
                host = external_node['address']
                try:
                    data = requests.get(url=external_node["address"] + "/fetch-blockchain")
                    block_list = []
                    for block in data.json():
                        header = BlockHeader()
                        header.previous_block_hash = block["header"]["previous_block_hash"]
                        header.nonce = block["header"]["nonce"]
                        block_list.append(Block(header, block["transactions"]))
                    self.node.blockchain.blocks = block_list
                    break
                except Exception as e:
                    print(f"Error with node {host}, couldn't find active target host. {str(e)}")
        else:
            header = BlockHeader()
            self.blocks = [Block(header, [])]
