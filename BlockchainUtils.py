from Crypto.Hash import SHA256
import json
import jsonpickle

class BlockchainUtils():

    @staticmethod
    def hash(data):
        dataString = json.dumps(data)
        byteString = dataString.encode('utf-8')
        dataHash = SHA256.new(byteString)
        return dataHash

    @staticmethod
    def encode(object):
        return jsonpickle.encode(object, unpicklable=True)

    @staticmethod
    def decode(object):
        return jsonpickle.decode(object)