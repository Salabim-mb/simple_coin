import hashlib
import time
from utils.block import Block

max_nonce = 2 ** 32 # 4 billion


def proof_of_work(block: Block, difficulty_bits):
    # calculate the difficulty target
    target = 2 ** (256-difficulty_bits)
    print("Started proof of work")
    for nonce in range(max_nonce):
        block.header.nonce = nonce
        hash_result = hashlib.sha256(str(block.as_json()).encode('utf-8')).hexdigest()
        # check if this is a valid result, below the target
        if int(hash_result, 16) < target:
            print(f"Success with nonce {nonce}")
            print(f'Hash is {hash_result}')
            return nonce
    print(f'Failed after {nonce} tries')
    return nonce