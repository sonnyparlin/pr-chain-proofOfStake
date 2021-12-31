from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from config import TX_TYPE_EXCHANGE, TX_TYPE_TRANSFER, Pprint

def main():
    blockchain = Blockchain()
    pool = TransactionPool()

    alice = Wallet()
    bob = Wallet()
    exchange = Wallet()
    forger = Wallet()

    exchange_transaction = exchange.create_transaction(alice.address, 10, TX_TYPE_EXCHANGE)

    if not pool.transaction_exists(exchange_transaction):
        pool.add_transaction(exchange_transaction)
    
    covered_transaction = \
        blockchain.get_covered_transactions_set(pool.transactions)
    last_hash = BlockchainUtils.hash(
        blockchain.blocks[-1].payload()).hexdigest()
    block_count = blockchain.blocks[-1].block_count + 1
    blockOne = Block(covered_transaction, last_hash, 
        forger.address, block_count)
    blockchain.add_block(blockOne)

    # alice wants to send 5 tokens to bob
    transaction = alice.create_transaction(
        bob.address, 5, TX_TYPE_TRANSFER)

    if not pool.transaction_exists(transaction):
        pool.add_transaction(transaction)

    covered_transaction = \
        blockchain.get_covered_transactions_set(pool.transactions)
    last_hash = BlockchainUtils.hash(
        blockchain.blocks[-1].payload()).hexdigest()
    block_count = blockchain.blocks[-1].block_count + 1
    blockTwo = Block(covered_transaction, last_hash, 
        forger.address, block_count)
    blockchain.add_block(blockTwo)

    Pprint(blockchain.to_json())

if __name__ == '__main__':
    main()