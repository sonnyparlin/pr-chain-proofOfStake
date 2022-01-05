import pytest
from Block import Block
from Wallet import Wallet
from Blockchain import Blockchain


def test_genesis():
    genesis = Block.genesis()
    assert isinstance(genesis, Block)
    assert genesis.block_count == 0
    assert genesis.transactions == []
    assert genesis.last_hash == 'first'
    assert genesis.hash == '*prawn-genesis-hash*'

def test_new_block_is_valid_block():
    blockchain = Blockchain()
    data = []
    hash = "*****"
    genesis_hash = blockchain.blocks[-1].hash
    block = Block(data, genesis_hash, hash, Wallet(), 1)
    blockchain.add_block(block)
    new_block = blockchain.blocks[-1]
    
    assert isinstance(new_block, Block)
    assert new_block.transactions == data
    assert new_block.last_hash == genesis_hash
    assert new_block.block_count == blockchain.blocks[-2].block_count + 1

def test_new_block_is_not_valid():
    blockchain = Blockchain()
    data = []
    hash = "*****"
    genesis_hash = blockchain.blocks[-1].hash
    block = Block(data, genesis_hash + 'foo', hash, Wallet(), 2)
    
    with pytest.raises(Exception, match = 'The block last_hash must be correct'):
        blockchain.add_block(block)