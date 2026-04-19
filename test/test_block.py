import time
import hashlib
from block import Block

def test_block_init():
    block = Block(1, "prev_hash", 123.0, ["data"], 5)
    assert block.index == 1
    assert block.previous_hash == "prev_hash"
    assert block.timestamp == 123.0
    assert block.data == ["data"]
    assert block.nonce == 5

def test_block_compute_hash():
    block = Block(1, "prev", 123.0, [], 0)
    expected_str = "1prev123.0[]0"
    expected_hash = hashlib.sha256(expected_str.encode()).hexdigest()
    assert block.compute_hash() == expected_hash

def test_block_is_valid():
    block = Block(1, "prev", 123.0, [], 0)
    # mock the compute_hash
    block.compute_hash = lambda: "000abc"
    assert block.is_valid(3) == True
    assert block.is_valid(4) == False

def test_proof_of_work_non_verbose(capsys):
    block = Block(1, "prev", 123.0, [], 0)
    block.proof_of_work(2, verbose=False)
    assert block.compute_hash().startswith("00")
    captured = capsys.readouterr()
    assert "mined in" in captured.out

def test_proof_of_work_verbose(capsys):
    block = Block(1, "prev", 123.0, [], 0)
    block.proof_of_work(1, verbose=True)
    assert block.compute_hash().startswith("0")
    captured = capsys.readouterr()
    assert "=== Starting Proof of Work ===" in captured.out
    assert "VALID BLOCK FOUND!" in captured.out

def test_block_repr():
    block = Block(1, "prev", 123.0, ["tx"], 0)
    rep = repr(block)
    assert "Block(Index: 1" in rep
    assert "Data: ['tx']" in rep
