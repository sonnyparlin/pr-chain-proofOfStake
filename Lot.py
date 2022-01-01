from BlockchainUtils import BlockchainUtils

class Lot():

    def __init__(self, publicKeyString, iteration, last_hash):
        self.publicKeyString = str(publicKeyString)
        self.iteration = iteration
        self.last_hash = last_hash
    
    def lot_hash(self):
        hash_data = self.publicKeyString + self.last_hash
        for _ in range(self.iteration):
            hash_data = BlockchainUtils.hash(hash_data).hexdigest()
        return hash_data