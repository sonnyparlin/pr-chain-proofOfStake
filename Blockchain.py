from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake
from Wallet import Wallet
from config import TX_EXCHANGE, TX_REWARD, TX_STAKE
import copy

class Blockchain():
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.pos = ProofOfStake()

    def add_block(self, block):
        #print('adding via add_block()')
        if self.blocks[-1].hash != block.last_hash:
            raise Exception('The block last_hash must be correct')

        self.add_accounts(block.transactions)

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
        return self.blocks[-1].block_count == block.block_count - 1

    def last_block_hash_valid(self, block):
        latest_blockchain_block_hash = self.blocks[-1].hash
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
        return Wallet.calculate_balance(self, publickey)
    
    def get_info(self, publickey, balance):
        return self.accountModel.get_info(publickey, balance)

    def transaction_covered(self, transaction):
        if transaction.type == TX_EXCHANGE or transaction.type == TX_REWARD:
            # Run crypto checks here to verify exchange wallet
            return True
        sender_balance = Wallet.calculate_balance(self, transaction.sender_address)
        return sender_balance >= transaction.amount

    def add_accounts(self, transactions):
        for transaction in transactions:
            self.add_account(transaction)

    def add_account(self, transaction):       
        amount = transaction.amount
        if transaction.type == TX_STAKE:
            self.accountModel.add_or_update_account(transaction.sender_address, transaction.sender_public_key, transaction.receiver_address, transaction.amount)
            self.pos.update(transaction.sender_public_key, amount)
        else:
            self.accountModel.add_or_update_account(transaction.sender_address, transaction.sender_public_key)
            self.accountModel.add_or_update_account(transaction.receiver_address, transaction.receiver_public_key)
                    
    def next_forger(self):
        last_hash = copy.copy(self.blocks[-1].hash)
        return self.pos.forger(last_hash)

    def create_block(self, transaction_from_pool, forger_wallet):
        covered_transactions = self.get_covered_transactions_set(
            transaction_from_pool)
        tx_list=[]
        for tx in covered_transactions:
            tx_list.append(tx.__str__())
        hash_str = ''.join(tx_list)
        hash = BlockchainUtils.hash(hash_str).hexdigest()
        last_hash = self.blocks[-1].hash
        
        new_block = forger_wallet.create_block(
            covered_transactions,
            last_hash,
            hash,
            len(self.blocks))

        self.add_accounts(new_block.transactions)
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
        return forger_public_key == proposed_block_forger
            
    def transactions_valid(self, transactions):
        covered_transactions = self.get_covered_transactions_set(transactions)
        return len(covered_transactions) == len(transactions)