import hashlib
import time


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: int):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()

    def compute_hash(self) -> str:
        transaction_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        return hashlib.sha256(transaction_string.encode()).hexdigest() 

test_transaction = Transaction("sender", "recipient", 1000)
print(test_transaction.compute_hash())