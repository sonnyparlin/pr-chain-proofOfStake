import pytest
from Block import Block
from Wallet import Wallet
from Blockchain import Blockchain
from AccountModel import AccountModel
from Transaction import Transaction
import time

def test_genesis():
    genesis = Block.genesis()
    assert isinstance(genesis, Block)
    assert genesis.block_count == 0
    assert genesis.transactions == []
    assert genesis.last_hash == 'first'
    assert genesis.hash == '*prawn-genesis-hash*'

@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    accountModel = AccountModel()
    exchange = Wallet()
    alice = Wallet()
    forger = Wallet()
    bob = Wallet()
    fred = Wallet()

    transaction = Transaction(exchange, alice, 100, 'EXCHANGE')
    transaction2 = Transaction(alice, bob, 5, 'TRANSFER')
    transaction3 = Transaction(alice, fred, 5, 'TRANSFER')

    transactions = [transaction, transaction2, transaction3]

    for tx in transactions:
        if tx.sender_address not in accountModel.accounts:
                accountModel.add_account(tx.sender_address, tx.sender_public_key)
            
        if tx.receiver_address not in accountModel.accounts:
            accountModel.add_account(tx.receiver_address, tx.receiver_public_key)
    
    accountModel.update_balance(alice.address, 100)
    accountModel.update_balance(alice.address, -10)
    accountModel.update_balance(bob.address, 5)
    accountModel.update_balance(fred.address,5)
    block = Block(transactions, blockchain.blocks[-1].hash, 'foo-hash', forger, 1)
    blockchain.add_block(block)

    accountModel.update_balance(alice.address, -5)
    accountModel.update_balance(bob.address, 5)
    transaction_second_block = Transaction(alice, bob, 5, 'TRANSFER')
    transactions_second_block = [transaction_second_block]

    block = Block(transactions_second_block, blockchain.blocks[-1].hash, 'foo-hash2', forger, 2)
    blockchain.add_block(block)

    accountModel.update_balance(alice.address, -5)
    accountModel.update_balance(bob.address, 5)
    transaction_third_block = Transaction(alice, bob, 5, 'TRANSFER')
    transactions_third_block = [transaction_third_block]

    block = Block(transactions_third_block, blockchain.blocks[-1].hash, 'foo-hash3', forger, 3)
    blockchain.add_block(block)

    return [blockchain, accountModel, alice]

def test_alot_of_blocks(blockchain_three_blocks):
    blockchain = blockchain_three_blocks[0]
    accountModel = blockchain_three_blocks[1]
    alice = blockchain_three_blocks[2]
    bob = Wallet()
    forger= Wallet()
    exchange = Wallet()
    transaction = Transaction(exchange, alice, 10000, 'EXCHANGE')

    for tx in [transaction]:            
        if tx.receiver_address not in accountModel.accounts:
            accountModel.add_account(tx.receiver_address, tx.receiver_public_key)

    accountModel.update_balance(alice.address, 10000)
    block = Block([transaction], blockchain.blocks[-1].hash, 'foo-hash4', forger, 4)
    blockchain.add_block(block)

    start = time.time()
    tx = Transaction(alice, bob, 1, 'TRANSFER')
    if tx.receiver_address not in accountModel.accounts:
        accountModel.add_account(tx.receiver_address, tx.receiver_public_key)

    for i in range(10000):
        if blockchain.transaction_covered(tx):
            accountModel.update_balance(alice.address, -1)
            accountModel.update_balance(bob.address, 1)
            block = Block([tx], blockchain.blocks[-1].hash, 'foo-hash4-'+str(i), forger, 4+i)
            blockchain.add_block(block)
    end = time.time()
    elapsed = end-start

    assert len(blockchain.blocks) == 10004
    assert accountModel.get_balance(alice.address) == 80
    assert accountModel.get_balance(bob.address) == 10000
    assert elapsed < 5

def test_alot_of_transactions_in_one_block(blockchain_three_blocks):
    blockchain = blockchain_three_blocks[0]
    accountModel = blockchain_three_blocks[1]
    alice = blockchain_three_blocks[2]
    bob = Wallet()
    forger= Wallet()
    exchange = Wallet()
    tx = Transaction(exchange, alice, 1000, 'EXCHANGE')

    if tx.receiver_address not in accountModel.accounts:
        accountModel.add_account(tx.receiver_address, tx.receiver_public_key)

    accountModel.update_balance(alice.address, 10000)
    block = Block([tx], blockchain.blocks[-1].hash, 'foo-hash4', forger, 4)
    blockchain.add_block(block)

    start = time.time()
    txs = []
    
    tx = Transaction(alice, bob, 1, 'TRANSFER')
    if tx.receiver_address not in accountModel.accounts:
        accountModel.add_account(tx.receiver_address, tx.receiver_public_key)
    for i in range(10000):
        if blockchain.transaction_covered(tx):
            txs.append(tx)
    accountModel.update_balance(alice.address, -10000)
    accountModel.update_balance(bob.address, 10000)
    
    block = Block(txs, blockchain.blocks[-1].hash, 'foo-hash5', forger, 5)
    blockchain.add_block(block)
    end = time.time()
    elapsed = end-start

    assert len(blockchain.blocks) == 6
    assert accountModel.get_balance(alice.address) == 80
    assert accountModel.get_balance(bob.address) == 10000
    assert elapsed < 1

def test_block_1_is_valid_block(blockchain_three_blocks):
    blockchain = blockchain_three_blocks[0]
    assert isinstance(blockchain, Blockchain)
    block = blockchain.blocks[1]
    transactions = blockchain.blocks[1].transactions
    assert isinstance(block, Block)
    assert block.transactions == transactions
    assert block.last_hash == Block.genesis().hash
    assert block.block_count == blockchain.blocks[0].block_count + 1
    assert len(blockchain.blocks) == 4

def test_string_of_last_hashes_are_valid(blockchain_three_blocks):
    blockchain = blockchain_three_blocks[0]
    accountModel = blockchain_three_blocks[1]
    alice = blockchain_three_blocks[2]
    bob = Wallet()
    forger= Wallet()
    exchange = Wallet()
    transaction = Transaction(exchange, alice, 10000, 'EXCHANGE')

    for tx in [transaction]:            
        if tx.receiver_address not in accountModel.accounts:
            accountModel.add_account(tx.receiver_address, tx.receiver_public_key)

    accountModel.update_balance(alice.address, 10000)
    block = Block([transaction], blockchain.blocks[-1].hash, 'foo-hash4', forger, 4)
    blockchain.add_block(block)

    start = time.time()
    tx = Transaction(alice, bob, 1, 'TRANSFER')
    if tx.receiver_address not in accountModel.accounts:
        accountModel.add_account(tx.receiver_address, tx.receiver_public_key)

    for i in range(10000):
        if blockchain.transaction_covered(tx):
            accountModel.update_balance(alice.address, -1)
            accountModel.update_balance(bob.address, 1)
            block = Block([tx], blockchain.blocks[-1].hash, 'foo-hash4-'+str(i), forger, 4+i)
            blockchain.add_block(block)
    end = time.time()
    elapsed = end-start

    for i in range(len(blockchain.blocks)):
        if i == 0:
            next
        else:
            assert blockchain.blocks[i].last_hash == blockchain.blocks[i-1].hash

    assert elapsed < 1
    assert accountModel.get_balance(alice.address) == 80


def test_balances_are_correct(blockchain_three_blocks):
    accountModel = blockchain_three_blocks[1]
    alice = blockchain_three_blocks[2]
    assert accountModel.get_balance(alice.address) == 80

def test_new_block_is_not_valid():
    blockchain = Blockchain()
    data = []
    hash = "*****"
    genesis_hash = blockchain.blocks[-1].hash
    block = Block(data, genesis_hash + 'foo', hash, Wallet(), 2)
    
    with pytest.raises(Exception, match = 'The block last_hash must be correct'):
        blockchain.add_block(block)