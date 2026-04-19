import time
import hashlib
from transaction import Transaction

def test_transaction_init():
    tx = Transaction("Alice", "Bob", 100)
    assert tx.sender == "Alice"
    assert tx.recipient == "Bob"
    assert tx.amount == 100
    assert tx.timestamp <= time.time()

def test_transaction_compute_hash():
    tx = Transaction("Alice", "Bob", 100)
    tx.timestamp = 123456789.0
    expected_hash_string = "AliceBob100123456789.0"
    expected_hash = hashlib.sha256(expected_hash_string.encode()).hexdigest()
    assert tx.compute_hash() == expected_hash
