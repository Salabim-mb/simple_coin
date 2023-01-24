from utils.block import Block
import requests
from utils.block_header import BlockHeader
import json
from anytree import Walker


class Blockchain:
    """
    Class for blockchain representation
    """
    def __init__(self, node):
        self.node = node
        self.blocks: [Block] = []

    def fetch_blocks(self):
        """
        Fetch blocks (used by new nodes that joined the blockchain distributed system)
        :return:
        """
        if len(self.node.node_list) > 1:
            for external_node in self.node.node_list:
                if external_node['name'] == self.node.name:
                    continue
                host = external_node['address']
                try:
                    data = requests.get(url=external_node["address"] + "/fetch-blockchain")
                    for block in data.json():
                        header = BlockHeader()
                        header.previous_block_hash = block["header"]["previous_block_hash"]
                        header.nonce = block["header"]["nonce"]
                        if header.previous_block_hash:
                            print("Adding new block")
                            if self.node.blockchain.blocks[-1].header.previous_block_hash == header.previous_block_hash:
                                self.node.blockchain.blocks.append(Block(header, json.loads(block["transactions"]), self.node.blockchain.blocks[-2]))
                            else:
                                self.node.blockchain.blocks.append(
                                    Block(header, json.loads(block["transactions"]), self.node.blockchain.blocks[-1]))
                        else:
                            self.node.blockchain.blocks.append(Block(header, json.loads(block["transactions"]), None))
                    break
                except Exception as e:
                    print(f"Error with node {host}, couldn't find active target host. {str(e)}")
        else:
            header = BlockHeader()
            self.blocks = [Block(header, [], None)]

    def get_longest_blockchain(self):
        """
        Walk from root node to leaf nodes to find longest path in blockchain
        :return:
        """
        if len(self.blocks) < 3:
            return self.blocks
        longest_blockchain: [Block] = []
        longest_path_length = 0
        for block in self.blocks:
            w = Walker()
            path = w.walk(self.blocks[0], block)
            non_empty_path_elements = [el for el in path if el]
            if len(non_empty_path_elements) > longest_path_length:
                longest_blockchain = non_empty_path_elements
        longest_blockchain_converted: [Block] = []
        for node_tuple in longest_blockchain:
            if type(node_tuple) is tuple:
                for el in node_tuple:
                    longest_blockchain_converted.append(el)
            else:
                longest_blockchain_converted.append(node_tuple)
        return longest_blockchain_converted

    def calculate_sum(self):
        sum = 0
        for block in self.get_longest_blockchain():
            for transaction in block["transactions"]:
                output = transaction["outputs"]
                for amount in output:
                    sum += amount["amount"]

