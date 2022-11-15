from multiprocessing import Process, Queue
import time
from utils.block_header import BlockHeader
from utils.block import Block
import hashlib
import requests
import base64


max_nonce = 2 ** 32  # 4 billion


def mine(miner, node) -> None:
    """
    Infinitely running function calculating complex hashes used for mining cryptocurrency
    :return:
    """
    print("Miner daemon start")
    while True:
        miner.reset = False
        candidate_block = miner.prepare_candidate_block(node)
        if miner.reset:
            continue
        for external_node in node.node_list:
            # send to everyone, including self
            host = external_node['address']
            try:
                time.sleep(1)
                requests.post(url=host + "/candidate-block", json=candidate_block.as_json(), headers={
                    'X-Pub-Key': base64.b64encode(node.pub_key.to_string()),
                    'Origin': node.address
                })
            except Exception as e:
                print(f"Error with node {host}, couldn't find active target host. {str(e)}")


class Miner:
    """
    Class containing own thread to mine cryptocurrency, part of block
    """

    def __init__(self):
        self.difficulty_bits = 5
        self.reset = False
        self.queue = None
        self.miner_thread = None

    def prepare_candidate_block(self, node) -> Block or None:
        """
        Creates and validates (with proof of work) a new candidate block based on the last element of blockchain
        :param: node
        :return: new block calculated from the previous one in blockchain
        """
        try:
            last_block: Block = node.blockchain.blocks[-1]
        except IndexError:
            last_block = Block(BlockHeader(), [])
        last_block_hash = hashlib.sha256(str(last_block.as_json()).encode('utf-8')).hexdigest()
        candidate_block_header = BlockHeader()
        candidate_block_header.previous_block_hash = last_block_hash
        candidate_block = Block(candidate_block_header, node.transaction_pool)
        nonce = self.proof_of_work(candidate_block)
        if nonce == -1:
            return
        candidate_block.header.nonce = nonce
        # print("Candidate block" + str(candidate_block.as_json()))
        return candidate_block

    def verify_candidate_block(self, candidate_block: {}) -> bool:
        """
        Checks if calculated hash value (in hexadecimal) is smaller than target value
        :param candidate_block: source block used for calculating current hash
        :return: previously described number comparison flag - True if hash result is smaller than target
        """
        target = 2 ** (256 - self.difficulty_bits)
        hash_result = hashlib.sha256(str(candidate_block).encode('utf-8')).hexdigest()
        # check if this is a valid result, below the target
        return int(hash_result, 16) < target

    def proof_of_work(self, block: Block) -> int:
        """
        Calculate next hash in blockchain as proof of work for entire network
        :param block: block that needs updating by setting nonce flag
        :return: iteration index when hashing succeeded or max nonce
        """
        # calculate the difficulty target
        target = 2 ** (256 - self.difficulty_bits)
        # print("Started proof of work")
        nonce = -1
        for nonce in range(max_nonce):
            if self.reset:
                return -1
            block.header.nonce = nonce
            hash_result = hashlib.sha256(str(block.as_json()).encode('utf-8')).hexdigest()
            # check if this is a valid result, below the target
            if int(hash_result, 16) < target:
                # print(f"Success with nonce {nonce}")
                # print(f'Hash is {hash_result}')
                return nonce
        # print(f'Failed after {nonce} tries')
        return nonce

    def run(self, node) -> None:
        """
        Worker for maintaining a multiprocess mining
        :return:
        """
        self.queue = Queue()
        self.miner_thread = Process(name='miner_thread', target=mine, args=(self, node,))
        self.miner_thread.start()

