import time
from blockchain import Blockchain
from block import Block
from transaction import Transaction

def test_blockchain_init():
    bc = Blockchain(2)
    assert bc.difficulty == 2
    assert bc.chain == []
    assert bc.unconfirmed_transactions == []

def test_create_genesis_block(capsys):
    bc = Blockchain(1)
    bc.create_genesis_block()
    assert len(bc.chain) == 1
    assert bc.chain[0].index == 0
    assert bc.chain[0].data == "Genesis Block"
    captured = capsys.readouterr()
    assert "Block(Index: 0" in captured.out

def test_last_block():
    bc = Blockchain(1)
    bc.create_genesis_block()
    assert bc.last_block() == bc.chain[0]

def test_add_block_invalid_previous_hash():
    bc = Blockchain(1)
    bc.create_genesis_block()
    block = Block(1, "wrong_hash", time.time(), [], 0)
    assert bc.add_block(block) == False
    assert len(bc.chain) == 1

def test_add_block_invalid_proof():
    bc = Blockchain(2) # Require difficulty 2
    bc.create_genesis_block()
    
    # create a block without valid proof
    block = Block(1, bc.last_block().compute_hash(), time.time(), [], 0)
    # forcefully set nonce so hash is unlikely to have 2 zeros
    while block.compute_hash().startswith("00"):
        block.nonce += 1
    assert bc.add_block(block) == False
    assert len(bc.chain) == 1

def test_add_block_valid():
    bc = Blockchain(1)
    bc.create_genesis_block()
    block = Block(1, bc.last_block().compute_hash(), time.time(), [], 0)
    block.proof_of_work(bc.difficulty)
    assert bc.add_block(block) == True
    assert len(bc.chain) == 2

def test_add_transaction():
    bc = Blockchain(1)
    tx = Transaction("A", "B", 10)
    bc.add_transaction(tx)
    assert len(bc.unconfirmed_transactions) == 1
    assert bc.unconfirmed_transactions[0] == tx

def test_mine_block_no_transactions(capsys):
    bc = Blockchain(1)
    bc.create_genesis_block()
    result = bc.mine_block()
    assert result is None
    captured = capsys.readouterr()
    assert "No transactions to mine." in captured.out

def test_mine_block_with_transactions():
    bc = Blockchain(1)
    bc.create_genesis_block()
    tx = Transaction("A", "B", 10)
    bc.add_transaction(tx)
    mined_block = bc.mine_block()
    assert mined_block is not None
    assert len(bc.chain) == 2
    assert len(bc.unconfirmed_transactions) == 0
    assert mined_block.data == [tx]

def test_is_chain_valid():
    bc = Blockchain(1)
    bc.create_genesis_block()
    tx = Transaction("A", "B", 10)
    bc.add_transaction(tx)
    bc.mine_block()
    assert bc.is_chain_valid() == True

def test_is_chain_invalid_tampered_data():
    bc = Blockchain(1)
    bc.create_genesis_block()
    tx = Transaction("A", "B", 10)
    bc.add_transaction(tx)
    bc.mine_block()
    
    # Tamper with the chain
    bc.chain[1].data = []
    assert bc.is_chain_valid() == False

def test_is_chain_invalid_tampered_hash():
    bc = Blockchain(1)
    bc.create_genesis_block()
    tx = Transaction("A", "B", 10)
    bc.add_transaction(tx)
    bc.mine_block()
    
    # Tamper with previous hash
    bc.chain[1].previous_hash = "fake"
    assert bc.is_chain_valid() == False

def test_is_chain_invalid_tampered_proof():
    bc = Blockchain(1)
    bc.create_genesis_block()
    tx = Transaction("A", "B", 10)
    bc.add_transaction(tx)
    bc.mine_block()
    
    # Make block invalid by incrementing nonce after it was mined
    bc.chain[1].nonce += 1
    while bc.chain[1].is_valid(bc.difficulty):
        bc.chain[1].nonce += 1
    assert bc.is_chain_valid() == False
