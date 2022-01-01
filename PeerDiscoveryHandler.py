import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils

class PeerDiscoveryHandler():

    def __init__(self, node):
        self.socket_communication = node

    def start(self):
        status_thread = threading.Thread(target=self.status, args=())
        status_thread.start()
        discovery_thread = threading.Thread(target=self.discovery, args=())
        discovery_thread.start()

    def status(self):
        while True:
            print('Current Connections: \n')
            for peer in self.socket_communication.peers:
                print(str(peer.ip) + ':' + str(peer.port))
            time.sleep(10)

    def discovery(self):
        while True:
            handshake_message = self.handshake_message()
            self.socket_communication.broadcast(handshake_message)
            time.sleep(10)
    
    def handshake(self, connect_node):
        handshake_message = self.handshake_message()
        self.socket_communication.send(connect_node, handshake_message)

    def handshake_message(self):
        own_socket_connector = self.socket_communication.socketConnector
        own_peers = self.socket_communication.peers
        data = own_peers
        message_type = 'DISCOVERY'
        message = Message(own_socket_connector, message_type, data)
        encoded_message = BlockchainUtils.encode(message)
        return encoded_message

    def handle_message(self, message):
        peersSocketConnector = message.sender_connector
        peersPeerList = message.data
        new_peer = True

        for peer in self.socket_communication.peers:
            if peer.equals(peersSocketConnector):
                new_peer = False
        
        if new_peer == True:
            self.socket_communication.peers.append(peersSocketConnector)

        for peersPeer in peersPeerList:
            peer_known = False
            for peer in self.socket_communication.peers:
                if peer.equals(peersPeer):
                    peer_known = True
            if not peer_known and not peersPeer.equals(self.socket_communication.socketConnector):
                self.socket_communication.connect_with_node(
                    peersPeer.ip, peersPeer.port)