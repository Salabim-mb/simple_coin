class BlockHeader:
    """
    Stateless class for aggregating header type
    """

    def __init__(self):
        self.previous_block_hash = None
        self.nonce = None
