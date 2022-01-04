from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake
import copy

class Blockchain():
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.pos = ProofOfStake()

    def add_block(self, block):
        self.execute_transactions(block.transactions)
        if self.blocks[-1].block_count < block.block_count:
            self.blocks.append(block)

    def to_json(self):
        data = {}
        json_blocks = []
        for block in self.blocks:
            json_blocks.append(block.to_json())
        data['blocks'] = json_blocks
        return data

    def block_count_valid(self, block):
        if self.blocks[-1].block_count == block.block_count - 1:
            return True
        else:
            return False

    def last_block_hash_valid(self, block):
        latest_blockchain_block_hash = copy.copy(self.blocks[-1].hash)
        return latest_blockchain_block_hash == block.last_hash

    def get_covered_transactions_set(self, transactions):
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
            else:
                print('Transaction is not covered by sender')
        return covered_transactions

    def get_balance(self, publickey):
        return self.accountModel.get_balance(publickey)
    
    def get_info(self, publickey):
        return self.accountModel.get_info(publickey)

    def transaction_covered(self, transaction):
        if transaction.type == 'EXCHANGE':
            # Run crypto checks here to verify exchange wallet
            return True
        sender_balance = self.accountModel.get_balance(
            transaction.sender_address)
        return sender_balance >= transaction.amount

    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)

    def execute_transaction(self, transaction):

        if transaction.sender_address not in self.accountModel.balances.keys():
            self.accountModel.add_account(transaction.sender_address, transaction.sender_public_key)
        
        if transaction.receiver_address not in self.accountModel.balances.keys():
            self.accountModel.add_account(transaction.receiver_address, transaction.receiver_public_key)

        sender_address = transaction.sender_address
        receiver_address = transaction.receiver_address
        amount = transaction.amount

        if transaction.type == 'STAKE':
            if sender_address == receiver_address:
                self.pos.update(transaction.sender_public_key, amount)
                self.accountModel.update_balance(
                    sender_address,
                    -amount)
        else:              
            self.accountModel.update_balance(
                sender_address,
                -amount)
            self.accountModel.update_balance(
                receiver_address, 
                amount)
                    
    def next_forger(self):
        last_hash = copy.copy(self.blocks[-1].hash)
        return self.pos.forger(last_hash)

    def create_block(self, transaction_from_pool, forger_wallet):
        covered_transactions = self.get_covered_transactions_set(
            transaction_from_pool)
        self.execute_transactions(covered_transactions)
        tx_list=[]
        for tx in covered_transactions:
            tx_list.append(tx.__str__())
        hash_str = ''.join(tx_list)
        hash = BlockchainUtils.hash(hash_str).hexdigest()
        last_hash = copy.copy(self.blocks[-1].hash)
        
        new_block = forger_wallet.create_block(
            covered_transactions,
            last_hash,
            hash,
            len(self.blocks))

        # todo:
        # reward the forger
        
        self.blocks.append(new_block)
        return new_block

    def transaction_exists(self, transaction):
        for block in self.blocks:
            for block_transaction in block.transactions:
                if transaction.equals(block_transaction):
                    return True
        return False

    def forger_valid(self, block):
        forger_public_key = self.pos.forger(block.last_hash)
        proposed_block_forger = block.forger
        if forger_public_key == proposed_block_forger:
            return True
        else:
            return False

    def transactions_valid(self, transactions):
        covered_transactions = self.get_covered_transactions_set(transactions)
        if len(covered_transactions) == len(transactions):
            return True
        else:
            return False