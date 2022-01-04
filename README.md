### Start the app
First create and activate your virtual environment with:
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Generate a wallet from the command line
```
python Wallet.py <name>
```
This will generate 3 files
* name_publicKey.pem
* name_privateKey.pem
* name_address.txt

Move these files into the keys/ folder and then start the app as follows.
```
python Main.py localhost 10001 5100 keys/name_privateKey.pem
```
This starts the root node for the blockchain.

Create a staker's node:
```
python Wallet.py staker
```
Move key files into the keys directory.

In a second terminal window start a new staking node:
```
python Main.py localhost 10002 5101 keys/staker_privateKey.pem 
```

Start an additional non staking nodes (as many as you want, just make sure they have unique node and api ports if you run them on the same machine)
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
@route('/txhistory/<address>', methods=['GET'])
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
exchange = Wallet() # special wallet used for forging coins
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

### TODO

1. Proof of stake upgrade:
Currently, if the validating node is unavailable, transactions don't get added to the blockchain. We need to have a fall back for when a staker's node is unavailable.
2. Front end design
3. Liquidity???
4. Onboarding/offboarding solutions
5. ICO???