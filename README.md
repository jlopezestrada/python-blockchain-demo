# Python Blockchain Demonstration

## Overview
The Python Blockchain Demo is a modular command-line application that implements fundamental blockchain concepts. Designed as an educational tool, it demonstrates how a decentralized ledger operates at a basic level without relying on external network protocols or persistent storage dependencies.

The system emphasizes two core design philosophies:
*   **Immutability:** Utilizing SHA-256 cryptographic hashes to ensure that any alteration to a block's data or sequence invalidates the entire chain.
*   **Simplicity:** Relying exclusively on Python's standard library (`hashlib`, `time`, `logging`, `argparse`) to maintain focus on the core logical mechanisms of a blockchain.

## Architecture & Key Components

The architecture is divided into two primary logical domains: the **Core Logic** and the **Application Interface**.

### Core Logic (`src/`)
The foundational building blocks of the blockchain ecosystem:

*   **`Transaction` (`src/transaction.py`):** The simplest data structure representing a transfer of value. It encapsulates the sender, recipient, amount, and a timestamp, and can generate a unique cryptographic hash for the transaction.
*   **`Block` (`src/block.py`):** An immutable record within the chain. It stores transaction data (or arbitrary payload for the Genesis block), metadata (timestamp, index), a cryptographic link to the preceding block (`previous_hash`), and a `nonce`. The `Block` class implements the core Proof of Work algorithm necessary for mining.
*   **`Blockchain` (`src/blockchain.py`):** The central orchestrator. It maintains the chronological sequence of validated `Block` objects (the ledger) and an internal mempool for unconfirmed transactions. It handles the logic for packaging transactions, executing Proof of Work to mine new blocks, and recursively validating the integrity of the entire chain.

### Application Interface (`main.py`)
The user-facing Command Line Interface (CLI) provides an interactive demonstration of the blockchain's capabilities. It utilizes `argparse` for configuration and executes a predefined synchronous workflow that initializes the chain, queues dummy transactions, triggers the mining processes, validates the final state, and exports a formatted ledger to standard output.

## Installation and Setup

This project requires Python 3.x. No third-party dependencies are required to run the core application.

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd python-blockchain-demo
    ```
2.  (Optional but recommended) Create a virtual environment for testing:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

## Usage

Execute the demonstration via the CLI entry point, `main.py`.

### Standard Execution
```bash
python main.py
```

### Configuration Flags
*   **`--difficulty <int>`**: Sets the target difficulty for the Proof of Work algorithm (the number of leading zeros required in a valid block hash). The default is `4`.
*   **`--verbose`**: Toggles the logging level to `DEBUG`, exposing the internal hash generation attempts during the mining process.

**Example:**
```bash
python main.py --difficulty 5 --verbose
```

## Testing Strategy

The project includes a comprehensive test suite utilizing `pytest` and `pytest-cov`, achieving **100% code coverage** across all core modules and the CLI interface.

To run the tests and generate a coverage report:
1. Ensure the virtual environment is active.
2. Install the testing dependencies:
    ```bash
    pip install pytest pytest-cov
    ```
3. Execute the test suite:
    ```bash
    pytest --cov=src --cov=main.py --cov-report=term-missing test/
    ```

The test suite rigorously evaluates component initialization, hash computation, Proof of Work validation, chain integrity checks against malicious tampering, and command-line argument handling.

## Development Conventions

*   **Structure:** Core logic resides in `src/`, testing in `test/`, and the entry point is at the root.
*   **Style:** Adheres to standard Python object-oriented patterns with appropriate type hinting.

## Future Improvements
*   **Graphical User Interface (GUI):** Implementation of a web-based or desktop interface for interactive visualization of the ledger and mining processes.
*   **Advanced Logic:** Integration of peer-to-peer (P2P) networking, wallet management using public/private key cryptography, smart contracts, or Proof of Stake consensus algorithms.