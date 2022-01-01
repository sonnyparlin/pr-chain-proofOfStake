from BlockchainUtils import BlockchainUtils
from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
import time

class Node():

    def __init__(self, ip, port, key = None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()
        if key is not None:
            self.wallet.from_key(key)

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)
    
    def startAPI(self, port):
        self.api = NodeAPI()
        self.api.inject_node(self)
        self.api.start(port)

    def handle_transaction(self, transaction):
        add_or_update = False
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = Wallet.valid_signature(data, signature, signer_public_key)

        transaction_exists = self.transaction_pool.transaction_from_pool(transaction.sender_address)
        transaction_in_block = self.blockchain.transaction_exists(transaction)


        if not transaction_exists and not transaction_in_block and signature_valid:
            self.transaction_pool.add_transaction(transaction)
            add_or_update = True
        elif transaction_exists and signature_valid:
            add_or_update = True
            self.transaction_pool.update_transaction(transaction_exists, transaction.receiver_address, transaction.amount)
        
        if add_or_update:
            message = Message(self.p2p.socketConnector, 'TRANSACTION', transaction)
            encoded_message = BlockchainUtils.encode(message)
            self.p2p.broadcast(encoded_message)
            forgingRequired = self.transaction_pool.forger_required()
            if forgingRequired:
                self.forge()

    def forge(self):
        forger = self.blockchain.next_forger()
        if forger == self.wallet.publicKeyString():
            print('I am the next forger')
            block = self.blockchain.create_block(self.transaction_pool.transactions, self.wallet)
            self.transaction_pool.remove_from_pool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            encoded_message = BlockchainUtils.encode(message)
            self.p2p.broadcast(encoded_message)
        else:
            print('i am not the next forger')
            time.sleep(10)
        return
