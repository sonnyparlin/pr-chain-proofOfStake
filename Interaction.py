from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests
from config import TX_EXCHANGE, TX_TRANSFER, TX_STAKE

def post_transaction(sender, receiver, amount, type):
    transaction = sender.create_transaction(receiver, amount, type=type)
    url = 'http://localhost:5100/transact'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.json())

if __name__ == '__main__':
    bob = Wallet()
    alice = Wallet()
    alice.from_key('keys/stakerPrivateKey.pem')
    exchange = Wallet()
    paul = Wallet()

    #forger: genesis
    post_transaction(exchange, alice, 100, TX_EXCHANGE)
    post_transaction(exchange, bob, 100, TX_EXCHANGE)
    post_transaction(exchange, bob, 10, TX_EXCHANGE)

    # forger: probably alice
    post_transaction(alice, alice, 25, TX_STAKE)
    post_transaction(alice, bob, 1, TX_TRANSFER)
    post_transaction(alice, bob, 1, TX_TRANSFER)

    post_transaction(alice, bob, 1, 'TRANSFER')
    post_transaction(alice, bob, 1, 'TRANSFER')
    post_transaction(alice, bob, 1, 'TRANSFER')

    post_transaction(alice, bob, 1, 'TRANSFER')
    post_transaction(alice, bob, 1, 'TRANSFER')
    post_transaction(alice, bob, 1, 'TRANSFER')

    post_transaction(alice, bob, 1, 'TRANSFER')
    post_transaction(alice, bob, 1, 'TRANSFER')
    post_transaction(alice, bob, 1, 'TRANSFER')
    
    