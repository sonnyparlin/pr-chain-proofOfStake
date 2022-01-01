import uuid
import time
import copy

class Transaction():

    def __init__(self, sender, receiver, amount, type):
        self.sender_address = sender.address
        self.sender_public_key = sender.publicKeyString()
        self.receiver_address = receiver.address
        self.receiver_public_key = receiver.publicKeyString()
        self.amount = amount
        self.outputs = self.create_output(
            self.receiver_address, 
            self.amount
        )
        self.type = type
        self.id = uuid.uuid1().hex  
        self.timestamp = time.time()
        self.signature = ''

    def create_output(self, receiver, amount):
        """
        Structure the output data for the transaction.
        """
        outputs = {}
        outputs[receiver] = amount
        return outputs

    def to_json(self):
        return self.__dict__

    def add_signature(self, signature):
        self.signature = signature

    def payload(self):
        json_representation = copy.deepcopy(self.to_json())
        json_representation['signature'] = ''
        return json_representation

    def equals(self, transaction):
        return transaction.id == self.id