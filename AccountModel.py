

class AccountModel():

    def __init__(self):
        self.accounts = []
        self.account = {}

    def add_account(self, address, publicKey):
        if not address in self.accounts:
            self.accounts.append(address)
            self.account[address]=[{'balance': 0,
                            'address': address,
                            'publicKey': publicKey}]

    def get_balance(self, address):
        if address in self.account:
            return self.account[address][0]['balance']
        else:
            return 0

    def get_info(self, address):
        if address in self.account:
            return self.account[address][0]
        else:
            return {"address": "Not found", "balance": 0, "publicKey": "None"}

    def update_balance(self, address, amount):
        self.account[address][0]['balance'] += amount