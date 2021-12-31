from Crypto.Hash import SHA256
import json

class BlockchainUtils():

    @staticmethod
    def hash(data):
        dataString = json.dumps(data)
        byteString = dataString.encode('utf-8')
        dataHash = SHA256.new(byteString)
        return dataHash