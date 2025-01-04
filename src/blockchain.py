import time

from block import Block


class Blockchain:
    def __init__(self, difficulty=1):
        self.difficulty = difficulty
        self.chain = []
        self.unconfirmed_transactions = []

    def create_genesis_block(self):
        genesis_block = Block(0, None, time.time(), "Genesis Block")
        print(genesis_block)
        genesis_block.proof_of_work(self.difficulty)
        print(genesis_block)
        self.chain.append(genesis_block)

blockchain_demo = Blockchain(1)
blockchain_demo.create_genesis_block()
