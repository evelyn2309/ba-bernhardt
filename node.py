from connection import *


class Node(object):
    def __init__(self):
        self.conn = Connection()

    def setup_node(self, address, port):
        """
        Fucntion to setup a node.
        :param address: must be string.
        :param port: must be int.
        :return: None.
        """

        self.conn.connect_server(address, port)


n = Node()
# modify here the IP-address and the port
n.setup_node("192.168.2.226", 5563)
