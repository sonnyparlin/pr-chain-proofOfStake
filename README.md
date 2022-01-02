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