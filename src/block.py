import hashlib
import time
from datetime import datetime


class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce

    def compute_hash(self):
        """Return the hash of the block by encoding its properties."""
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def is_valid(self, difficulty):
        """Check if the block is valid based on the hash."""
        return self.compute_hash().startswith("0" * difficulty)

    def proof_of_work(self, difficulty, verbose=False):
        """
        Performs the proof-of-work algorithm with an option to enable or disable logging.

        Args:
            difficulty (int): The difficulty level (number of leading zeroes required in the hash).
            verbose (bool): If True, logs detailed output during the process.
        """
        prefix = "0" * difficulty
        if verbose:
            print("=== Starting Proof of Work ===")
            print(f"Block Index: {self.index}")
            print(f"Difficulty Level: {difficulty}")
            print(f"Timestamp: {self.timestamp}")
            print(f"Initial Nonce: {self.nonce}")
            print("-" * 40)

        start_time = time.time()

        while not self.compute_hash().startswith(prefix):
            if verbose:
                print(f"Trying Nonce: {self.nonce} | Hash: {self.compute_hash()}")
            self.nonce += 1

        elapsed_time = time.time() - start_time

        if verbose:
            print("-" * 40)
            print("*****VALID BLOCK FOUND!*****")
            print(f"Block Details: {self}")
            print(f"Proof of Work completed in {elapsed_time:.2f} seconds.")
            print("=== Proof of Work Complete ===")
        else:
            print(f"***** Block {self.index} mined in {elapsed_time:.2f} seconds *****")
            print(f"Hash: {self.compute_hash()}")
            print(f"Nonce: {self.nonce}")

    def __repr__(self):
        """Provides a detailed string representation of the block for debugging."""
        return (
            f"Block("
            f"Index: {self.index}, "
            f"Hash: {self.compute_hash()}, "
            f"Previous Hash: {self.previous_hash}, "
            f"Timestamp: {datetime.fromtimestamp(self.timestamp)}, "
            f"Data: {self.data}, "
            f"Nonce: {self.nonce}"
            f")"
        )
