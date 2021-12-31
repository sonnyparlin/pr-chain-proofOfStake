import uuid
import time
import copy

class Transaction():
  
    def __init__(self, sender_address, receiver_address, amount, type):
        self.sender_address = sender_address
        self.receiver_address = receiver_address
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex  
        self.timestamp = time.time()
        self.signature = ''

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