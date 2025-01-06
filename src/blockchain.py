import time

from block import Block
from transaction import Transaction


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

    def add_transaction(self, transaction: Transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine_block(self) -> Block:
        if not self.unconfirmed_transactions:
            print("No transactions to mine.")
            return None

        new_block = Block(
            index=len(self.chain),
            previous_hash=self.last_block().compute_hash(),
            timestamp=time.time(),
            data=self.unconfirmed_transactions
        )
        new_block.proof_of_work(self.difficulty)
        self.add_block(new_block)
        self.unconfirmed_transactions = []
        return new_block

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i]
            if current.previous_hash != previous.compute_hash():
                return False
            if not current.is_valid(self.difficulty):
                return False
        return True

blockchain_demo = Blockchain(1)
blockchain_demo.create_genesis_block()
print(blockchain_demo.chain)
