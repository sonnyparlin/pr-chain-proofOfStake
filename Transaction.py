import uuid
import time
import copy

class Transaction():

    def __init__(self, 
                sender=None,
                sender_public_key=None,
                receiver=None,
                amount=None, 
                outputs=None, 
                type=None):
        self.sender_address = sender.address
        self.sender_public_key = sender.publicKeyString()
        self.receiver_address = receiver.address
        self.amount = amount
        self.outputs = outputs or self.create_output(
            receiver.address, 
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
        #return self.__dict__
        data = {}
        data['sender_address'] = self.sender_address
        data['outputs'] = self.outputs
        data['amount'] = self.amount
        data['signature'] = self.signature
        data['type'] = self.type
        data['id'] = self.id
        data['timestamp'] = self.timestamp
        data['signature'] = self.signature
        return data

    def add_signature(self, signature):
        self.signature = signature

    def payload(self):
        json_representation = copy.deepcopy(self.to_json())
        json_representation['signature'] = ''
        return json_representation

    def equals(self, transaction):
        return transaction.id == self.id