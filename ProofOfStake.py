from Lot import Lot
from BlockchainUtils import BlockchainUtils

class ProofOfStake():

    def __init__(self):
        self.stakers = {}
        self.set_genesis_node_stake()

    def set_genesis_node_stake(self):
        genesis_public_key = open('keys/genesisPublicKey.pem', 'r').read()
        self.stakers[genesis_public_key] = 1

    def update(self, publicKeyString, stake):
        if publicKeyString in self.stakers.keys():
            self.stakers[publicKeyString] += stake
        else:
            self.stakers[publicKeyString] = stake 

    def get(self, publicKeyString):
        if publicKeyString in self.stakers.keys():
            return self.stakers[publicKeyString]
        else:
            return None

    def validatorLots(self, seed):
        lots = []
        for validator in self.stakers.keys():
            for stake in range(self.get(validator)):
                lots.append(Lot(validator, stake+1, seed))
        return lots

    def winner_lot(self, lots, seed):
        winner_lot = None
        least_offset = None
        hash = BlockchainUtils.hash(seed).hexdigest()
        reference_hash_int_value = int(hash, 16)
        # print("reference_hash_int_value: ", reference_hash_int_value)
        for lot in lots:
            lot_int_value = int(lot.lot_hash(), 16)
            offset = abs(lot_int_value - reference_hash_int_value)
            if least_offset is None or offset < least_offset:
                least_offset = offset
                winner_lot = lot
        return winner_lot

    def forger(self, last_block_hash):
        lots = self.validatorLots(last_block_hash)
        winner_lot = self.winner_lot(lots, last_block_hash)
        return winner_lot.publicKeyString