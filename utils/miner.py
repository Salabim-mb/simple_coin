import random
import threading
import time
from utils.block_header import BlockHeader
from utils.block import Block
import hashlib
import requests
import base64
from utils.wallet.Transaction import Transaction

max_nonce = 2 ** 32 # 4 billion

MINING_REWARD = 2


class Miner:
    def __init__(self, node):
        self.difficulty_bits = 20
        self.node = node
        miner_thread = threading.Thread(name='miner_thread', target=self.mine)
        miner_thread.start()

    def mine(self):
        global reset
        time.sleep(10)
        while True:
            reset = False
            candidate_block = self.prepare_candidate_block()
            self.node.blockchain.blocks.append(candidate_block)
            m = Transaction()
            m.create_input(MINING_REWARD,"%032x" % random.getrandbits(256), base64.b64encode(self.node.pub_key.to_string()).decode())
            m.create_output(MINING_REWARD, base64.b64encode(self.node.pub_key.to_string()).decode())
            self.node.wallet.balance += MINING_REWARD
            self.node.transaction_pool.append(m.as_json())
            if reset:
                continue
            for external_node in self.node.node_list:
                if external_node['name'] == self.node.name:
                    continue
                host = external_node['address']
                try:
                    requests.post(url=host + "/candidate-block", json=candidate_block.as_json(), headers={
                        'X-Pub-Key': base64.b64encode(self.node.pub_key.to_string()),
                        'Origin': self.node.address
                    })
                except Exception as e:
                    print(f"Error with node {host}, couldn't find active target host. {str(e)}")

    def prepare_candidate_block(self):
        try:
            last_block: Block = self.node.blockchain.blocks[-1]
        except IndexError:
            last_block_header = BlockHeader()
            last_block = Block(last_block_header, [])
        last_block_hash = hashlib.sha256(str(last_block).encode('utf-8')).hexdigest()
        candidate_block_header = BlockHeader()
        candidate_block_header.previous_block_hash = last_block_hash
        candidate_block = Block(candidate_block_header, self.node.transaction_pool)
        nonce = self.proof_of_work(candidate_block)
        if nonce == -1:
            return
        candidate_block.header.nonce = nonce
        print("Candidate block" + str(candidate_block.as_json()))
        return candidate_block

    def verify_candidate_block(self, candidate_block):
        target = 2 ** (256 - self.difficulty_bits)
        hash_result = hashlib.sha256(str(candidate_block).encode('utf-8')).hexdigest()
        # check if this is a valid result, below the target
        return int(hash_result, 16) < target

    def proof_of_work(self, block: Block):
        global reset
        # calculate the difficulty target
        target = 2 ** (256 - self.difficulty_bits)
        print("Started proof of work")
        for nonce in range(max_nonce):
            if reset:
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

