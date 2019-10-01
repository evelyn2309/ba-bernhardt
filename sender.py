from connection import *
from crypt import *


class Sender(object):
    def __init__(self, notified_server, participants_bittorrent):
        self.cr = Crypt()
        self.notified_server = notified_server
        self.participants_bittorrent = participants_bittorrent
        self.conn = Connection(participants_bittorrent)

    def restart(self):
        """
        Function to restart all nodes. Send RESTART-message to all.
        Uses: connection.py.
        :return: None.
        """

        for i in range(len(self.participants_bittorrent["ip"])):
            s = self.conn.setup_sender(self.participants_bittorrent["ip"][i], self.participants_bittorrent["port"][i])
            self.conn.send_receive(s, "RESTART")
            print("restart: " + str(i))
        print("restarted all")

    def kill(self):
        """
        Function to kill all nodes. Send KILL-message to all.
        Uses: connection.py.
        :return: None.
        """
        for i in range(len(self.participants_bittorrent["ip"])):
            s = self.conn.setup_sender(self.participants_bittorrent["ip"][i], self.participants_bittorrent["port"][i])
            self.conn.send_receive(s, "KILL")
            print("kill: " + str(i))
        print("killed all")

    def construct_package(self, message):
        """
        Function to construct an send the enpryted notification package.
        Uses: hashing.py, connection.py and crypt.py.
        :param message: must be string.
        :return: None.
        """

        session_key_sender_n1 = self.cr.generate_session_key()
        session_key_sender_n2 = self.cr.generate_session_key()
        session_key_sender_receiver = self.cr.generate_session_key()

        inner_package = {
            "enc_package": self.cr.encrypt_message_aes(str({
                # hash the message as controll for receiver later
                "message": Hashing.hash_message(self.cr.encrypt_message_aes(message, session_key_sender_receiver))
            }), session_key_sender_receiver),
            "enc_key": self.cr.encrypt_message_rsa(session_key_sender_receiver, self.notified_server["ip"][3])
        }

        middle_package = {
            "enc_package": self.cr.encrypt_message_aes(str({
                "next": [self.notified_server["ip"][3], self.notified_server["port"][3]],
                "package": str(inner_package)
            }), session_key_sender_n2),
            "enc_key": self.cr.encrypt_message_rsa(session_key_sender_n2, self.notified_server["ip"][2])
        }

        outer_package = {
            "enc_package": self.cr.encrypt_message_aes(str({
                "next": [self.notified_server["ip"][2], self.notified_server["port"][2]],
                # send encrypted message for bittorrent to start node
                "message": [self.cr.encrypt_message_aes(message, session_key_sender_receiver),
                            self.participants_bittorrent],
                "package": str(middle_package)
            }), session_key_sender_n1),
            "enc_key": self.cr.encrypt_message_rsa(session_key_sender_n1, self.notified_server["ip"][1])
        }
        # print(outer_package)
        return outer_package

    def connect_send(self, message):
        """
        Function to connect sender to a server.
        Uses: connection.py
        :param message:
        :return: s.
        """
        s = self.conn.setup_sender(self.notified_server["ip"][1], self.notified_server["port"][1])
        package = self.construct_package(message)
        self.conn.send_receive(s, str(package))
        return s
