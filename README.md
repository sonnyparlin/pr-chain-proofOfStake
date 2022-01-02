### Start the app
First activate your environment with:
```
source env/bin/activate
```

Start the first node
```
python Main.py localhost 10001 5100 keys/genesisPrivateKey.pem
```

Start a new staking node
```
python Main.py localhost 10002 5101 keys/stakerPrivateKey.pem 
```

Start an additional non staking node (as many as you want, just make sure they have unique node and api ports)
```
python Main.py localhost 10002 5101
```

### Test the app
```
python Interaction.py
```

### Endpoints
```python
@route('/info', methods=['GET'])
def info(self):
    return 'This is the beginning of our API', 200

@route('/wallet/<address>', methods=['GET'])
def get_wallet_info(self, address):
    balance = node.handle_balance_request(address)
    json_string = {"address": address, "balance": balance}
    return jsonify(json_string), 200

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
```