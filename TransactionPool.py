

class TransactionPool():

    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def transaction_exists(self, transaction):
        # Check if this tranactions exists in the list of transactions
        for pool_transaction in self.transactions:
            if pool_transaction.equals(transaction):
                return True
        return False

    def update_transaction(self, transaction, receiver, amount):
        """
        Update the transaction with a new or existing recipient
        """
        for address in list(transaction.outputs.keys()):
            if address == receiver:
                transaction.outputs[receiver] += amount
            else:
                transaction.outputs[receiver] = amount


    def transaction_from_pool(self, sender_address):
        for pool_transaction in self.transactions:
            if pool_transaction.sender_address == sender_address:
                return pool_transaction

    def remove_from_pool(self, transactions):
        new_pool_transactions = []
        for pool_transaction in self.transactions:
            insert = True
            for transaction in transactions:
                if pool_transaction.equals(transaction):
                    insert = False
            if insert == True:
                new_pool_transactions.append(pool_transaction)
        self.transactions = new_pool_transactions