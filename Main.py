from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
from Node import Node
from config import TX_TYPE_EXCHANGE, TX_TYPE_TRANSFER, Pprint
import sys

def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])
    api_port = int(sys.argv[3])
    key_file = None
    if len(sys.argv) > 4:
        key_file = sys.argv[4]

    node = Node(ip, port, key_file)
    node.startP2P()
    node.startAPI(api_port)

    

if __name__ == '__main__':
    main()