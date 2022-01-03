from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from BlockchainUtils import BlockchainUtils
from Transaction import Transaction
from Block import Block
import sys

class Wallet():

    def __init__(self):
        self.keyPair = RSA.generate(2048)
        h=SHA256.new(self.keyPair.public_key().exportKey().hex().encode('utf-8'))
        self.address = 'pv1' + h.hexdigest()[0:41]
    
    def from_key(self, file):
        key = ''
        with open(file, 'r') as key_file:
            key = RSA.importKey(key_file.read())
        self.keyPair = key
        h=SHA256.new(self.keyPair.public_key().exportKey().hex().encode('utf-8'))
        self.address = 'pv1' + h.hexdigest()[0:41]

    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemeObject.sign(dataHash)
        return signature.hex()        

    def publicKeyString(self):
        return self.keyPair.publickey().exportKey('PEM').decode('utf-8')

    def create_transaction(self, receiver, amount, type):
        transaction = Transaction(self, receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.add_signature(signature)
        return transaction

    def create_block(self, transactions, last_hash, hash, block_count):
        block = Block(transactions, last_hash, hash,
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

    @staticmethod
    def create_wallet_and_export_keys(filename):
        wallet = Wallet()
        with open(filename + '_privateKey.pem', "wb") as file:
            file.write(wallet.keyPair.exportKey('PEM'))
            file.close()

        with open(filename + '_publicKey.pem', "wb") as file:
            file.write(wallet.keyPair.publickey().exportKey('PEM'))
            file.close()

        with open(filename + '_address.txt', "wb") as file:
            file.write(wallet.address.encode('utf8'))
            file.close()

def main():
    Wallet.create_wallet_and_export_keys(sys.argv[1])

if __name__ == '__main__':
    main()