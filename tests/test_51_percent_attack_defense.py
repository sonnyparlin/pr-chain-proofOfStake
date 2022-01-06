import pytest
from Block import Block
from Wallet import Wallet
from Blockchain import Blockchain
from AccountModel import AccountModel
from Transaction import Transaction
from SocketCommunication import SocketCommunication
import time

def test_51_percent_attack():
    blockchain = Blockchain()
    accountModel = AccountModel()
    exchange = Wallet()
    alice = Wallet()
    forger = Wallet()
    bob = Wallet()
    forger= Wallet()
    exchange = Wallet()
    attacker = Wallet()
    evilchain = Blockchain()

    amount=1000
    tx = Transaction(exchange, attacker, amount, 'EXCHANGE')
    if tx.receiver_address not in accountModel.accounts:
        accountModel.add_account(tx.receiver_address, tx.receiver_public_key)

    block = Block([tx], evilchain.blocks[0].hash, 'foo-hash1', forger, 1)

    for i in range(10003):
        if evilchain.transaction_covered(tx):
            accountModel.update_balance(attacker.address, amount)
            block = Block([tx], evilchain.blocks[-1].hash, 'foo-hash-'+str(1+i), forger, 1+i)
            blockchain = block
            evilchain.add_block(block)
    
    assert(accountModel.get_balance(attacker.address)) == 10003000
    assert(len(evilchain.blocks)) == 10004

    #todo
    # use p2p software to replace the chain on the network
