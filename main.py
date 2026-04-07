"""Main entry point for the Python Blockchain Node CLI.

This module provides a command-line interface to demonstrate
the core functionality of the blockchain implementation, including
initialization, transaction processing, mining, and validation.
"""

import sys
import os
import argparse
import logging

# Add src to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from blockchain import Blockchain
from transaction import Transaction

def setup_logging(verbose: bool):
    """Configure the logging format and level for the CLI.

    Args:
        verbose (bool): If True, sets the logging level to DEBUG.
            Otherwise, sets it to INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def run_demo(difficulty: int):
    """Execute the standard blockchain demonstration flow.

    Initializes the blockchain, processes sample transactions,
    mines blocks, and validates the entire chain. Finally, it
    prints a formatted ledger of all blocks.

    Args:
        difficulty (int): The proof-of-work difficulty level
            (number of leading zeros required for a valid hash).
    """
    logger = logging.getLogger(__name__)
    
    logger.info("Initializing blockchain network with difficulty %d", difficulty)
    blockchain = Blockchain(difficulty=difficulty)
    blockchain.create_genesis_block()
    logger.info("Genesis block created and appended to the chain.")
    
    logger.info("Processing initial transaction batch...")
    tx1 = Transaction("Alice", "Bob", 50)
    tx2 = Transaction("Bob", "Charlie", 20)
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    logger.info("Transaction queued: %s -> %s (Amount: %d)", tx1.sender, tx1.recipient, tx1.amount)
    logger.info("Transaction queued: %s -> %s (Amount: %d)", tx2.sender, tx2.recipient, tx2.amount)
    
    logger.info("Mining Block 1...")
    blockchain.mine_block()
    
    logger.info("Processing secondary transaction batch...")
    tx3 = Transaction("Charlie", "Alice", 10)
    blockchain.add_transaction(tx3)
    logger.info("Transaction queued: %s -> %s (Amount: %d)", tx3.sender, tx3.recipient, tx3.amount)
    
    logger.info("Mining Block 2...")
    blockchain.mine_block()
    
    logger.info("Executing chain integrity validation...")
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        logger.info("Validation successful: The blockchain is secure and immutable.")
    else:
        logger.error("Validation failed: The blockchain data has been compromised.")
    
    print("\n" + "="*60)
    print("BLOCKCHAIN LEDGER EXPORT")
    print("="*60)
    for block in blockchain.chain:
        print(f"BLOCK {block.index}")
        print(f"Hash:          {block.compute_hash()}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Nonce:         {block.nonce}")
        
        if isinstance(block.data, str):
            print(f"Data:          {block.data}")
        else:
            print(f"Transactions:  {len(block.data)}")
            for tx in block.data:
                print(f"  -> {tx.sender} paid {tx.recipient} {tx.amount} units")
        print("-" * 60)

def main():
    """Parse command-line arguments and run the blockchain demo.
    
    Provides a CLI interface with options for setting the mining
    difficulty and enabling verbose logging.
    """
    parser = argparse.ArgumentParser(
        description="Python Blockchain Node CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--difficulty", 
        type=int, 
        default=4, 
        help="Proof-of-work difficulty level (number of leading zeros)"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose application logging"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    try:
        run_demo(args.difficulty)
    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Execution interrupted by user. Exiting...")
        sys.exit(1)

if __name__ == "__main__":
    main()
