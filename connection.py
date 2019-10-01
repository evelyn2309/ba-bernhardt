import socket
from crypt import *
from hashing import *
import time
from bittorrent import *


class Connection(object):

    def __init__(self, participants_bittorrent=None):
        if participants_bittorrent is None:
            participants_bittorrent = eval(open('participants_bittorrent.txt').read())

        # self.notified_server = notified_server
        self.participants_bittorrent = participants_bittorrent
        self.hash_value = ""
        self.session_key = ""
        self.address = ""
        self.port = 9999
        self.flood = False
        self.received_chunks = []
        self.cr = Crypt()

    def connect_server(self, address: str, port):
        """
        Function to connect a server.
        :param port: must be int.
        :param address: must be string.
        :return: None.
        """

        self.address = address
        self.port = port
        s = self.setup_server()
        while True:
            try:
                conn = self.setup_connection(s)
                print("Connection created.")
                self.data_transfer(conn, s)
                print("Wait for other messages...")
            except:
                break

    def setup_server(self):
        """
        Function to setup the server.
        Uses: socket.
        :return: s.
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created.")
        try:
            s.bind((self.address, self.port))
        except socket.error as msg:
            print(msg)
        print("Socket bind complete.")
        return s

    def setup_connection(self, s):
        """
        Function to septup connection.
        :param s: must be server.
        :return: conn.
        """

        s.listen(10)
        conn, address = s.accept()
        print("Connected to: " + address[0] + ":" + str(address[1]))
        return conn

    def data_transfer(self, conn, s):
        """
        Function for the data transfer.
        Receive data from the connection and react to it (start bittorrent process).
        Uses: hashing.py, crypt.py.
        :param conn: must be connection.
        :param s: must be server.
        :return: None.
        """

        print("Receive message...")
        whole_data = ""
        while True:
            data = conn.recv(1024)
            if data.decode('utf8') == 'KILL' or data.decode('utf8') == 'kill':
                print("Our server is shutting down.")
                s.close()
                conn.close()
                break
            if data.decode('utf8') == 'RESTART' or data.decode('utf8') == 'restart':
                print("Our server is restarted.")
                conn.close()
                self.hash_value = ""
                self.session_key = ""
                self.flood = False
                self.received_chunks = []
                break
            elif data.decode('utf8')[:10] == 'Bittorrent':
                print("Received Bittorrent Notification.")
                self.participants_bittorrent = eval(data.decode('utf8')[10:])
                break
            elif data.decode('utf8')[:2] == "BT":
                print("Bittorrent file received.")
                data = eval(data.decode('utf8')[2:])
                self.received_chunks.append(data)
                # flood file if node has not flooded his file to all other nodes
                if not self.flood:
                    #time.sleep(3)
                    self.flood_bittorrent(str(data))
                if self.check_receive_all(data["max_chunks"]):
                    file = self.load_bittorrent()
                    # check if the file is for the node
                    if Hashing.check_hash(self.hash_value, file):
                        print("Received Bittorrent File is for you. Decrypt Message with the old session key.")
                        encrypted_message = self.cr.decrypt_message_aes(file, self.session_key).decode('utf8')
                        print("The received anonymous message: ", encrypted_message)
                        # Write message in txt-file
                        open('message.txt', 'w').write(str(encrypted_message))
                    else:
                        print("Received Bittorrent File is not for you. Delete file.")
                        print("Thank you for using the anonymization network. Thanks to you anonymity on the internet"
                              " is possible. Maybe next time someone wants to send you a message. :)")
                    self.received_chunks = []
                    self.hash_value = ""
                    self.session_key = ""
                    self.flood = False
                    break
            else:
                if len(data) == 0 or data[-4:] == "EXIT":
                    break
                else:
                    data = data.decode('utf8')
                    whole_data += data

        if whole_data[-4:] == "EXIT":
            whole_data = whole_data[:-4]
        if whole_data != "":
            (next_node, message, package, session_key) = self.cr.evaluate_package(whole_data.encode('utf8'),
                                                                                  self.address)
            self.session_key = session_key
            if next_node != "":
                address = next_node[0]
                port = next_node[1]
                # print("Send package: ", package, " to next node ", address)
                self.send_package_to_next(address, port, package)
            else:
                print("You are the receiver.")
                self.hash_value = message
                print("Your hash to remember: ", self.hash_value)
            if message != "" and next_node != "":
                print("You are the Bittorrent-Start-Node. You have to inform all nodes.")
                mess = message[0]
                self.participants_bittorrent = message[1]
                self.inform_nodes()
                self.send_bittorrent(mess)
                time.sleep(15)
                print("Thank you for using the anonymization network. Thanks to you anonymity on the internet"
                      " is possible. Maybe next time someone wants to send you a message. :)")

    def send_package_to_next(self, address: str, port: int, package):
        """
        Function to send the given pacage to the next node.
        :param address: must be string.
        :param port: must be int.
        :param package: encrypted bytes.
        :return: None.
        """

        s = self.setup_sender(address, port)
        # print("Sending package to next.")
        self.send_receive(s, package.decode('utf8'))

    def setup_sender(self, address, port):
        """
        Function to setup the sender.
        Uses: socket.
        :param address:
        :param port:
        :return: s.
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connect to: ", address, port)
        s.connect((address, port))
        return s

    def send_receive(self, s, message: str):
        """
        Function to send a message.
        :param s: must be server.
        :param message: must be string.
        :return: None
        """

        if message == 'EXIT' or message == 'exit' or message == 'KILL' or message == 'kill':
            s.send(message.encode('utf8'))
        else:
            s.send(message.encode('utf8'))
            # print("Data has been send.")

    def send_bittorrent(self, message):
        """
        Function to build and send chunks to every participant.
        Uses: bittorrent.py.
        :param message: encrypted message must be string.
        :return: None.
        """

        print("Start Bittorent Process. Send ", message)
        number_participants = len(self.participants_bittorrent["ip"]) - 1
        chunks = Bittorrent.chunk_it(message, number_participants)  # all server excluding the bittorrent start node
        i = 0
        chunks_numbered = []
        for c in chunks:
            chunks_numbered.append({"number": i, "chunk": c, "max_chunks": number_participants})
            i += 1
        for j in range(1, len(self.participants_bittorrent["ip"])):
            s = self.setup_sender(self.participants_bittorrent["ip"][j], self.participants_bittorrent["port"][j])
            self.send_receive(s, "BT" + str(chunks_numbered[j - 1]))
        print("Send Bittorrent files to every participant.")

    def flood_bittorrent(self, chunk):
        """
        Fuction to float a file via Bittorrent from one node to all other participants.
        :param chunk: must be string.
        :return: None.
        """

        for i in range(1, len(self.participants_bittorrent["ip"])):
            print(self.participants_bittorrent["ip"][i])
            if self.participants_bittorrent["ip"][i] != self.address:
                s = self.setup_sender(self.participants_bittorrent["ip"][i], self.participants_bittorrent["port"][i])
                self.send_receive(s, "BT" + chunk)
        print("Floated chunk to all other nodes: ", chunk)
        self.flood = True

    def check_receive_all(self, number):
        """
        Function to check if the node received all chunks
        :param number: must be integer.
        :return: Boolean
        """
        return number == len(self.received_chunks)

    def load_bittorrent(self):
        """
        Function to combine the received chunks to one hash value.
        :return: final_message.
        """

        sorted_chunks = sorted(self.received_chunks, key=lambda k: k['number'])
        final_message = b''
        for c in sorted_chunks:
            chunk = c["chunk"]
            final_message += chunk
        return final_message

    def inform_nodes(self):
        """
        Function to inform all nodes in network for Bittorrent.
        :return: None.
        """

        # print("Wait a moment....")
        time.sleep(10)
        print("Inform all Nodes for Bittorrent.")
        for i in range(1, len(self.participants_bittorrent["ip"])):
            s = self.setup_sender(self.participants_bittorrent["ip"][i], self.participants_bittorrent["port"][i])
            self.send_receive(s, "Bittorrent" + str(self.participants_bittorrent))
