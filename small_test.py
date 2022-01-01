from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
from Node import Node
from config import TX_TYPE_EXCHANGE, TX_TYPE_TRANSFER, Pprint

def main():    
    blockchain = Blockchain()
    pool = TransactionPool()

    alice = Wallet()
    bob = Wallet()
    paul = Wallet()
    exchange = Wallet()
    forger = Wallet()

    def transact(wallet, receiver, amount, type):
        transaction = pool.transaction_from_pool(wallet.address)

        if not transaction:
            transaction = wallet.create_transaction(
                receiver=receiver, amount=amount, type=type)
            pool.add_transaction(transaction)
        else:
            pool.update_transaction(transaction, receiver, amount)

    def validate_and_add_to_the_blockchain():
        covered_transaction = \
        blockchain.get_covered_transactions_set(pool.transactions)
        last_hash = BlockchainUtils.hash(
        blockchain.blocks[-1].payload()).hexdigest()
        block_count = blockchain.blocks[-1].block_count + 1
        block = forger.create_block(covered_transaction, last_hash, block_count)
        blockchain.add_block(block)
        pool.remove_from_pool(block.transactions)

    transact(exchange, alice.address, 100, TX_TYPE_EXCHANGE)
    validate_and_add_to_the_blockchain()

    # alice wants to send 5 tokens to bob
    transact(alice, bob.address, 5, TX_TYPE_TRANSFER)
    transact(alice, bob.address, 5, TX_TYPE_TRANSFER)
    transact(alice, paul.address, 5, TX_TYPE_TRANSFER)
    validate_and_add_to_the_blockchain()

    Pprint(blockchain.to_json())

if __name__ == '__main__':
    main()
