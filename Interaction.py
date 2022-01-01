from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests
from config import TX_TYPE_EXCHANGE, TX_TYPE_TRANSFER

if __name__ == '__main__':
    bob = Wallet()
    alice = Wallet()
    exchange = Wallet()
    paul = Wallet()

    transaction = exchange.create_transaction(alice, 100, type=TX_TYPE_EXCHANGE)
    url = 'http://localhost:5100/transact'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.text)

    # transaction = alice.create_transaction(bob, 5, type=TX_TYPE_EXCHANGE)
    # url = 'http://localhost:5100/transact'
    # package = {'transaction': BlockchainUtils.encode(transaction)}
    # request = requests.post(url, json=package)
    # print(request.text)

    # transaction = alice.create_transaction(bob, 5, type=TX_TYPE_EXCHANGE)
    # url = 'http://localhost:5100/transact'
    # package = {'transaction': BlockchainUtils.encode(transaction)}
    # request = requests.post(url, json=package)
    # print(request.text)

    # transaction = alice.create_transaction(paul, 5, type=TX_TYPE_EXCHANGE)
    # url = 'http://localhost:5100/transact'
    # package = {'transaction': BlockchainUtils.encode(transaction)}
    # request = requests.post(url, json=package)
    # print(request.text)
