from Wallet import Wallet

class AccountModel():

    def __init__(self):
        self.accounts = []
        self.account = {}

    def add_or_update_account(self, address, publicKey, 
                                stake_wallet_address=None, staking=0):
        
        if not address in self.accounts:
            self.accounts.append(address)
        
        self.account[address]=[{'staking': staking,
                        'stake_wallet_address': stake_wallet_address,
                        'address': address,
                        'publicKey': publicKey}]

    def get_info(self, address, balance):
        self.account[address][0]['balance'] = balance
        return self.account[address]