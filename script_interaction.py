from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests
from config import TX_EXCHANGE, TX_TRANSFER, TX_STAKE
import time

def post_transaction(sender, receiver, amount, type):
    transaction = sender.create_transaction(receiver, amount, type=type)
    url = 'http://localhost:5001/transact'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.json())

if __name__ == '__main__':
    bob = Wallet()
    alice = Wallet()
    alice.from_key('keys/stakerPrivateKey.pem')
    alice_stake = Wallet()
    exchange = Wallet()
    paul = Wallet()
    bill = Wallet()

    #forger: genesis
    post_transaction(exchange, alice, 1000, TX_EXCHANGE)
    post_transaction(exchange, bob, 100, TX_EXCHANGE)
    post_transaction(exchange, bob, 10, TX_EXCHANGE)

    post_transaction(exchange, paul, 1000, TX_EXCHANGE)
    post_transaction(exchange, bill, 500, TX_EXCHANGE)
    post_transaction(alice, alice_stake, 25, TX_STAKE)

    post_transaction(paul, bob, 1, TX_TRANSFER)
    post_transaction(paul, bob, 2, TX_TRANSFER)
    post_transaction(paul, bob, 3, TX_TRANSFER)
    
    post_transaction(paul, bob, 4, TX_TRANSFER)
    post_transaction(paul, bob, 5, TX_TRANSFER)
    post_transaction(paul, bob, 6, TX_TRANSFER)

    post_transaction(paul, bob, 7, TX_TRANSFER)
    post_transaction(paul, bob, 8, TX_TRANSFER)
    post_transaction(paul, bob, 9, TX_TRANSFER)

    post_transaction(paul, bob, 10, TX_TRANSFER)
    post_transaction(paul, bob, 11, TX_TRANSFER)
    post_transaction(paul, bill, 10, TX_TRANSFER)
    
    