from BlockchainUtils import BlockchainUtils
from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message

class Node():

    def __init__(self, ip, port):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)
    
    def startAPI(self, port):
        self.api = NodeAPI()
        self.api.inject_node(self)
        self.api.start(port)

    def handle_transaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = Wallet.valid_signature(data, signature, signer_public_key)

        transaction_exists = self.transaction_pool.transaction_from_pool(transaction.sender_address)

        if not transaction_exists and signature_valid:
            self.transaction_pool.add_transaction(transaction)
        elif transaction_exists and signature_valid:
            self.transaction_pool.update_transaction(transaction_exists, transaction.receiver_address, transaction.amount)
        
        message = Message(self.p2p.socketConnector, 'TRANSACTION', transaction)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.broadcast(encoded_message)
