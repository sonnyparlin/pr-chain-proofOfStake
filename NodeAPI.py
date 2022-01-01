from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from BlockchainUtils import BlockchainUtils

node = None

class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, port):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host='0.0.0.0', port=port)

    def inject_node(self, injected_node):
        global node
        node = injected_node

    @route('/info', methods=['GET'])
    def info(self):
        return 'This is the beginning of our API', 200

    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        return node.blockchain.to_json(), 200

    @route('/transaction-pool', methods=['GET'])
    def transaction_pool(self):
        transactions = {}
        for ctr,transaction in enumerate(node.transaction_pool.transactions):
            transactions[ctr] = transaction.to_json()
        return jsonify(transactions), 200

    @route('/transact', methods=['POST'])
    def transact(self):
        values = request.get_json()
        if not 'transaction' in values:
            return "missing transaction values", 400
        
        transaction = BlockchainUtils.decode(values['transaction'])
        node.handle_transaction(transaction)
        response = {'message': 'Received transaction'}
        return jsonify(response), 201