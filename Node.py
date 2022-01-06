from Blockchain import Blockchain
from Transaction import Transaction
from TransactionPool import TransactionPool
from Wallet import Wallet
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI
from Message import Message
from BlockchainUtils import BlockchainUtils
from config import FORGE_REWARD, TX_REWARD, TX_STAKE, TX_TRANSFER, TX_EXCHANGE
import copy

class Node():

    def __init__(self, ip, port, key=None):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.blockchain = Blockchain()
        self.transaction_pool = TransactionPool()
        self.wallet = Wallet()
        if key is not None:
            self.wallet.from_key(key)

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)
    
    def startAPI(self, port):
        self.api = NodeAPI()
        self.api.inject_node(self)
        self.api.start(port)

    def handle_info_request(self, publickey, balance):
        return self.blockchain.get_info(publickey, balance)

    def get_balance(self, address):
        return Wallet.calculate_balance(self.blockchain, address)

    def handle_transaction_history(self, publickey):
        address_block_history = []
        for attr,val in self.blockchain.to_json().items():
            if attr == 'blocks':
                for block in val:
                    for tx in block['transactions']:
                        if publickey == tx['sender_address'] or \
                                publickey == tx['receiver_address']:
                            address_block_history.append(tx)
        return address_block_history


    def handle_transaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = Wallet.valid_signature(
            data, signature, signer_public_key)
        transaction_exists = self.transaction_pool.transaction_exists(transaction)
        transaction_in_block = self.blockchain.transaction_exists(transaction)
        if not transaction_exists and not transaction_in_block and signature_valid:
            self.transaction_pool.add_transaction(transaction)
            message = Message(self.p2p.socketConnector, 
                                'TRANSACTION', transaction)
            encoded_message = BlockchainUtils.encode(message)
            self.p2p.broadcast(encoded_message)
            if self.transaction_pool.forging_required():
                self.forge()

    def handle_block(self, block):
        forger = block.forger
        block_hash = block.payload()
        signature = block.signature

        block_count_valid = self.blockchain.block_count_valid(block)
        last_block_hash_valid = self.blockchain.last_block_hash_valid(block)
        forger_valid = self.blockchain.forger_valid(block)
        transactions_valid = self.blockchain.transactions_valid(block.transactions)
        signature_valid = Wallet.valid_signature(block_hash, signature, forger)

        if not block_count_valid:
            self.request_chain()
        if last_block_hash_valid and forger_valid and transactions_valid and signature_valid:
            self.blockchain.add_block(block)
            self.transaction_pool.remove_from_pool(block.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            self.p2p.broadcast(BlockchainUtils.encode(message))

    def handle_blockchain_request(self, requesting_node):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAIN', self.blockchain)
        encoded_message = BlockchainUtils.encode(message)
        self.p2p.send(requesting_node, encoded_message)

    def handle_blockchain(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.blockchain)
        local_block_count = len(local_blockchain_copy.blocks)
        incoming_blockchain_count = len(blockchain.blocks)

        if local_block_count < incoming_blockchain_count:
            for block_number, block in enumerate(blockchain.blocks):
                if block_number >= local_block_count:
                    print("Blocks are getting added via p2p update")
                    local_blockchain_copy.add_block(block)
                    self.transaction_pool.remove_from_pool(block.transactions)
            self.blockchain = local_blockchain_copy

    def forge(self):
        forger = self.blockchain.next_forger()
        if forger == self.wallet.publicKeyString():
            print('I am the next forger')
            block = self.blockchain.create_block(
                self.transaction_pool.transactions, self.wallet)
            self.transaction_pool.remove_from_pool(
                self.transaction_pool.transactions)
            message = Message(self.p2p.socketConnector, 'BLOCK', block)
            self.p2p.broadcast(BlockchainUtils.encode(message))
         
            # exchange = Wallet()
            # reward_tx=Transaction(exchange, self.wallet, FORGE_REWARD, TX_REWARD)
            # block = self.blockchain.create_block([reward_tx], self.wallet)
            # message = Message(self.p2p.socketConnector, 'BLOCK', block)
            # self.p2p.broadcast(BlockchainUtils.encode(message))
        else:
            print('i am not the next forger')
    
    def request_chain(self):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)
        self.p2p.broadcast(BlockchainUtils.encode(message))
