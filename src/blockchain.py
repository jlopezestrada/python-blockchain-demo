import time

from block import Block


class Blockchain:
    def __init__(self, difficulty: int = 1):
        self.difficulty = difficulty
        self.chain = []
        self.unconfirmed_transactions = []

    def create_genesis_block(self):
        genesis_block = Block(0, None, time.time(), "Genesis Block")
        print(genesis_block)
        genesis_block.proof_of_work(self.difficulty)
        print(genesis_block)
        self.chain.append(genesis_block)

    def last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, block: Block) -> bool:
        if block.previous_hash != self.last_block().compute_hash():
            return False
        if not block.is_valid(self.difficulty):
            return False
        self.chain.append(block)
        return True

blockchain_demo = Blockchain(1)
blockchain_demo.create_genesis_block()
print(blockchain_demo.chain)
