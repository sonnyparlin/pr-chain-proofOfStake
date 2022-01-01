from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from config import TX_TYPE_EXCHANGE

class Blockchain():
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()

    def add_block(self, block):
        self.execute_transactions(block.transactions)
        self.blocks.append(block)

    def to_json(self):
        data = {}
        json_blocks = []
        for block in self.blocks:
            json_blocks.append(block.to_json())
        data['blocks'] = json_blocks
        return data

    def block_count_valid(self, block):
        return self.blocks[-1].block_count == block.block_count -1

    def last_block_hash_valid(self, block):
        latest_blockchain_block_hash = BlockchainUtils.hash(
            self.blocks[-1].payload()).hexdigest()
        return latest_blockchain_block_hash == block.last_hash

    def get_covered_transactions_set(self, transactions):
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                print('Transaction is not covered by sender')
        return covered_transactions

    def transaction_covered(self, transaction):
        if transaction.type == TX_TYPE_EXCHANGE:
            return True
        sender_balance = self.accountModel.get_balance(
            transaction.sender_address)
        return sender_balance >= sum(transaction.outputs.values())

    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)

    def execute_transaction(self, transaction):
        sender = transaction.sender_address
        receivers = transaction.outputs.keys()

        for receiver in receivers:
            self.accountModel.update_balance(sender, - transaction.outputs[receiver])
            self.accountModel.update_balance(receiver, transaction.outputs[receiver])
        
        #print(self.accountModel.get_balance(transaction.sender_address))