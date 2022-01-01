import time
import copy

class Block():
    def __init__(self, transactions, last_hash, forger, block_count):
        self.block_count = block_count
        self.transactions = transactions
        self.last_hash = last_hash
        self.forger = forger
        self.timestamp = time.time()
        self.signature = ''

    def to_json(self):
        data = {}
        data['block_count'] = self.block_count
        data['last_hash'] = self.last_hash
        data['forger'] = self.forger
        data['timestamp'] = self.timestamp
        data['signature'] = self.signature
        json_transactions = []
        for transaction in self.transactions:
            json_transactions.append(transaction.to_json())
        data['transactions'] = json_transactions
        return data

    def payload(self):
        json_representation = copy.deepcopy(self.to_json())
        json_representation['signature'] = ''
        return json_representation

    def add_signature(self, signature):
        self.signature = signature

    @staticmethod
    def genesis():
        genesis_block = Block([], 'genesis_hash', 'genesis', 0)
        genesis_block.timestamp = 0
        return genesis_block