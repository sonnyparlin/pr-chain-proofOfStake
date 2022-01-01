from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from BlockchainUtils import BlockchainUtils
from Transaction import Transaction
from Block import Block
import uuid

class Wallet():

    def __init__(self):
        self.keyPair = RSA.generate(2048)
        self.address = 'prawnv1' + uuid.uuid1().hex

    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemeObject.sign(dataHash)
        return signature.hex()

    def publicKeyString(self):
        return self.keyPair.publickey().exportKey('PEM').decode('utf-8')

    def create_transaction(self, receiver, amount, type):
        transaction = Transaction(
        sender=self, receiver=receiver, amount=amount, outputs=None, type=type, sender_public_key=self.publicKeyString())
        signature = self.sign(transaction.payload())
        transaction.add_signature(signature)

        return transaction

    def create_block(self, transactions, last_hash, block_count):
        block = Block(transactions, last_hash, 
            self.address, block_count)
        signature = self.sign(block.payload())
        block.add_signature(signature)
        return block

    @staticmethod
    def valid_signature(data, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = BlockchainUtils.hash(data)
        publicKey = RSA.importKey(publicKeyString)
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)
        return signatureSchemeObject.verify(dataHash, signature)