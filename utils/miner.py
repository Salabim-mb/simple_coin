from multiprocessing import Process, Queue
import time
from utils.block_header import BlockHeader
from utils.block import Block
import hashlib
import requests
import base64


max_nonce = 2 ** 32  # 4 billion


class Miner:
    """
    Class containing own thread to mine cryptocurrency, part of block
    """

    def __init__(self, node):
        self.difficulty_bits = 5
        self.node = node
        self.reset = False
        self.queue = Queue()
        time.sleep(10)  # wait 10 secs before starting to mine
        self.__run()

    def __run(self) -> None:
        """
        [PRIVATE METHOD] Worker for maintaining a multiprocess mining
        :return:
        """
        miner_thread = Process(name='miner_thread', target=self.__mine)
        miner_thread.start()

    def __mine(self) -> None:
        """
        [PRIVATE METHOD] Infinitely running function calculating complex hashes used for mining cryptocurrency
        :return:
        """
        time.sleep(10)
        while True:
            self.reset = False
            candidate_block = self.prepare_candidate_block()
            if self.reset:
                continue
            for external_node in self.node.node_list:
                # send to everyone, including self
                host = external_node['address']
                try:
                    requests.post(url=host + "/candidate-block", json=candidate_block.as_json(), headers={
                        'X-Pub-Key': base64.b64encode(self.node.pub_key.to_string()),
                        'Origin': self.node.address
                    })
                except Exception as e:
                    print(f"Error with node {host}, couldn't find active target host. {str(e)}")

    def prepare_candidate_block(self) -> Block or None:
        """
        Creates and validates (with proof of work) a new candidate block based on the last element of blockchain
        :return: new block calculated from the previous one in blockchain
        """
        last_block: Block = self.node.blockchain.blocks[-1]
        last_block_hash = hashlib.sha256(str(last_block.as_json()).encode('utf-8')).hexdigest()
        candidate_block_header = BlockHeader()
        candidate_block_header.previous_block_hash = last_block_hash
        candidate_block = Block(candidate_block_header, self.node.transaction_pool)
        nonce = self.proof_of_work(candidate_block)
        if nonce == -1:
            return
        candidate_block.header.nonce = nonce
        print("Candidate block" + str(candidate_block.as_json()))
        return candidate_block

    def verify_candidate_block(self, candidate_block: Block) -> bool:
        """
        Checks if calculated hash value (in hexadecimal) is smaller than target value
        :param candidate_block: source block used for calculating current hash
        :return: previously described number comparison flag - True if hash result is smaller than target
        """
        target = 2 ** (256 - self.difficulty_bits)
        hash_result = hashlib.sha256(str(candidate_block.as_json()).encode('utf-8')).hexdigest()
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
        print("Started proof of work")
        for nonce in range(max_nonce):
            if self.reset:
                return -1
            block.header.nonce = nonce
            hash_result = hashlib.sha256(str(block.as_json()).encode('utf-8')).hexdigest()
            # check if this is a valid result, below the target
            if int(hash_result, 16) < target:
                print(f"Success with nonce {nonce}")
                print(f'Hash is {hash_result}')
                return nonce
        print(f'Failed after {nonce} tries')
        return nonce

