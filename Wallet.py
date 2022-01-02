from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from BlockchainUtils import BlockchainUtils
from Transaction import Transaction
from Block import Block
import uuid

class Wallet():

    def __init__(self):
        self.keyPair = RSA.generate(2048)
        h=SHA256.new(self.keyPair.public_key().exportKey().hex().encode('utf-8'))
        self.address = 'pv1' + h.hexdigest()[0:41]
        # self.address_list = []
        # self.address_list.append(self.address)
    
    def from_key(self, file):
        key = ''
        with open(file, 'r') as key_file:
            key = RSA.importKey(key_file.read())
        self.keyPair = key
        h=SHA256.new(self.keyPair.public_key().exportKey().hex().encode('utf-8'))
        self.address = 'pr1' + h.hexdigest()[0:41]

    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemeObject.sign(dataHash)
        return signature.hex()

    # def generate_new_address(self):
    #     self.address = 'prawnv1' + uuid.uuid1().hex
    #     self.address_list.append(self.address)

    def publicKeyString(self):
        return self.keyPair.publickey().exportKey('PEM').decode('utf-8')

    def create_transaction(self, receiver, amount, type):
        transaction = Transaction(self, receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.add_signature(signature)
        return transaction

    def create_block(self, transactions, last_hash, block_count):
        block = Block(transactions, last_hash, 
            self.publicKeyString(), block_count)
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