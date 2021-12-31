

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
