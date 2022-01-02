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

### Node API Endpoints
```python
@route('/info', methods=['GET'])
@route('/wallet/<address>', methods=['GET'])
@route('/blockchain', methods=['GET'])
@route('/transaction-pool', methods=['GET'])
@route('/transact', methods=['POST'])

# Example post request:
# - requires sender wallet, receiver wallet, amount and type
# - current transaction types: 'EXCHANGE', 'STAKE', and 'TRANSFER'
def post_transaction(sender, receiver, amount, type):
    transaction = sender.create_transaction(receiver, amount, type=type)
    url = 'http://localhost:5100/transact'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)
    print(request.json())

# example purchase by alice of 100 Prawns
alice = Wallet()
post_transaction(exchange, alice, 100, 'EXCHANGE')

# alice deicdes to become a forger/minter on the network
# and forge transactions via Proof of Stake to earn transaction
# fees   
post_transaction(alice, alice, 25, 'STAKE')
    
# This is a simple transfer from alice to bob of 1 prawn
bob = Wallet()
post_transaction(alice, bob, 1, 'TRANSFER')
```