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
        self.type = type
        self.id = uuid.uuid1().hex  
        self.timestamp = time.time()
        self.signature = ''

    def __str__(self):
        return f'{self.amount}:{self.id}:{self.receiver_address}:{self.sender_address}:{self.signature}:{self.timestamp}:{self.type}'

    def to_json(self):
        #return self.__dict__
        data = {}
        data['amount'] = self.amount
        data['id'] = self.id
        data['receiver_address'] = self.receiver_address
        data['sender_address'] = self.sender_address
        data['signature'] = self.signature
        data['timestamp'] = self.timestamp
        data['type'] = self.type
        return data

    def add_signature(self, signature):
        self.signature = signature

    def payload(self):
        json_representation = copy.deepcopy(self.to_json())
        json_representation['signature'] = ''
        return json_representation

    def equals(self, transaction):
        return transaction.id == self.id