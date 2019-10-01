import sys

from sender import *
import time

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qt


class SenderGui(qw.QWidget):
    def __init__(self):
        super().__init__()

        # Read out the notified server from txt-file
        self.notified_server = eval(open('notified_server.txt').read())
        self.notified_server_ip = []
        self.notified_server_port = []

        # Read out the bittorrent participants from txt-file
        self.participants_bittorrent = eval(open('participants_bittorrent.txt').read())
        self.participants_bittorrent_ip = []
        self.participants_bittorrent_port = []

        self.sender = Sender(self.notified_server, self.participants_bittorrent)

        # left site
        # headlines
        self.subtitle_left = qw.QLabel()
        self.subtitle_left.setText("Notifcation process")
        bold_font = qt.QFont()
        bold_font.setBold(True)
        self.subtitle_left.setFont(bold_font)

        # sender
        self.sender_lable = qw.QLabel()
        self.sender_lable.setText("Sender: ")
        self.sender_ip = qw.QLineEdit()
        self.sender_port = qw.QLineEdit()
        self.sender_ip.setReadOnly(True)
        self.sender_port.setReadOnly(True)

        # node 1
        self.node1_lable = qw.QLabel()
        self.node1_lable.setText("Node 1: ")
        self.node1_ip = qw.QLineEdit()
        self.node1_port = qw.QLineEdit()

        # node 2
        self.node2_lable = qw.QLabel()
        self.node2_lable.setText("Node 2: ")
        self.node2_ip = qw.QLineEdit()
        self.node2_port = qw.QLineEdit()

        # node 3
        self.node3_lable = qw.QLabel()
        self.node3_lable.setText("Receiver: ")
        self.node3_ip = qw.QLineEdit()
        self.node3_port = qw.QLineEdit()

        self.notified_server_ip.append(self.sender_ip)
        self.notified_server_ip.append(self.node1_ip)
        self.notified_server_ip.append(self.node2_ip)
        self.notified_server_ip.append(self.node3_ip)
        for i in range(len(self.notified_server["ip"])):
            self.notified_server_ip[i].setText(str(self.notified_server["ip"][i]))

        self.notified_server_port.append(self.sender_port)
        self.notified_server_port.append(self.node1_port)
        self.notified_server_port.append(self.node2_port)
        self.notified_server_port.append(self.node3_port)
        for i in range(len(self.notified_server["port"])):
            self.notified_server_port[i].setText(str(self.notified_server["port"][i]))

        # right site
        # overview
        self.subtitle_right = qw.QLabel()
        self.subtitle_right.setText("Bittorent process")
        self.subtitle_right.setFont(bold_font)

        # server 1
        self.server1_lable = qw.QLabel()
        self.server1_lable.setText("Startnode: ")
        self.server1_ip = qw.QLineEdit()
        self.server1_port = qw.QLineEdit()

        # server 2
        self.server2_lable = qw.QLabel()
        self.server2_lable.setText("Server 1: ")
        self.server2_ip = qw.QLineEdit()
        self.server2_port = qw.QLineEdit()

        # server 3
        self.server3_lable = qw.QLabel()
        self.server3_lable.setText("Server 2: ")
        self.server3_ip = qw.QLineEdit()
        self.server3_port = qw.QLineEdit()

        # server 4
        self.server4_lable = qw.QLabel()
        self.server4_lable.setText("Server 3: ")
        self.server4_ip = qw.QLineEdit()
        self.server4_port = qw.QLineEdit()

        # server 5
        self.server5_lable = qw.QLabel()
        self.server5_lable.setText("Server 4: ")
        self.server5_ip = qw.QLineEdit()
        self.server5_port = qw.QLineEdit()

        self.participants_bittorrent_ip.append(self.server1_ip)
        self.participants_bittorrent_ip.append(self.server2_ip)
        self.participants_bittorrent_ip.append(self.server3_ip)
        self.participants_bittorrent_ip.append(self.server4_ip)
        self.participants_bittorrent_ip.append(self.server5_ip)
        for i in range(len(self.participants_bittorrent["ip"])):
            self.participants_bittorrent_ip[i].setText(str(self.participants_bittorrent["ip"][i]))

        self.participants_bittorrent_port.append(self.server1_port)
        self.participants_bittorrent_port.append(self.server2_port)
        self.participants_bittorrent_port.append(self.server3_port)
        self.participants_bittorrent_port.append(self.server4_port)
        self.participants_bittorrent_port.append(self.server5_port)
        for i in range(len(self.participants_bittorrent["port"])):
            self.participants_bittorrent_port[i].setText(str(self.participants_bittorrent["port"][i]))

        # bottom
        # send message
        self.message = qw.QLineEdit()
        self.message.setText("Message...")

        # send button
        self.message_button = qw.QPushButton()
        self.message_button.setText("Send anonymous message")
        self.message_button.clicked.connect(self.send_message)

        # restart button
        self.restart_button = qw.QPushButton()
        self.restart_button.setText("Restart anonymization network")
        self.restart_button.clicked.connect(self.restart)
        self.restart_button.setDisabled(True)

        # left site
        self.layout_left_left = qw.QVBoxLayout()
        self.layout_left_left.addWidget(self.sender_lable)
        self.layout_left_left.addWidget(self.node1_lable)
        self.layout_left_left.addWidget(self.node2_lable)
        self.layout_left_left.addWidget(self.node3_lable)

        self.layout_left_middle = qw.QVBoxLayout()
        for node_ip in self.notified_server_ip:
            self.layout_left_middle.addWidget(node_ip)

        self.layout_left_right = qw.QVBoxLayout()
        for node_port in self.notified_server_port:
            self.layout_left_right.addWidget(node_port)

        self.layout_left = qw.QHBoxLayout()
        self.layout_left.addLayout(self.layout_left_left)
        self.layout_left.addStretch()
        self.layout_left.addLayout(self.layout_left_middle)
        self.layout_left.addStretch()
        self.layout_left.addLayout(self.layout_left_right)
        self.layout_left.addStretch()

        # right site
        self.layout_right_left = qw.QVBoxLayout()
        self.layout_right_left.addWidget(self.server1_lable)
        self.layout_right_left.addWidget(self.server2_lable)
        self.layout_right_left.addWidget(self.server3_lable)
        self.layout_right_left.addWidget(self.server4_lable)
        self.layout_right_left.addWidget(self.server5_lable)

        self.layout_right_middle = qw.QVBoxLayout()
        for bittorent_ip in self.participants_bittorrent_ip:
            self.layout_right_middle.addWidget(bittorent_ip)

        self.layout_right_right = qw.QVBoxLayout()
        for bittorent_port in self.participants_bittorrent_port:
            self.layout_right_right.addWidget(bittorent_port)

        self.layout_right = qw.QHBoxLayout()
        self.layout_right.addLayout(self.layout_right_left)
        self.layout_right.addStretch()
        self.layout_right.addLayout(self.layout_right_middle)
        self.layout_right.addStretch()
        self.layout_right.addLayout(self.layout_right_right)
        self.layout_right.addStretch()

        self.layout_middle = qw.QHBoxLayout()
        self.layout_middle.addLayout(self.layout_left)
        self.layout_middle.addStretch()
        self.layout_middle.addLayout(self.layout_right)
        self.layout_middle.addStretch()

        self.layout_under = qw.QVBoxLayout()
        self.layout_under.addWidget(self.message)
        self.layout_under.addWidget(self.message_button)
        self.layout_under.addWidget(self.restart_button)

        self.layout = qw.QVBoxLayout()
        self.layout_subtitles = qw.QHBoxLayout()
        self.layout_subtitles.addWidget(self.subtitle_left)
        self.layout_subtitles.addWidget(self.subtitle_right)

        self.layout.addLayout(self.layout_subtitles)
        self.layout.addStretch()
        self.layout.addLayout(self.layout_middle)
        self.layout.addStretch()
        self.layout.addLayout(self.layout_under)

        self.setLayout(self.layout)

    def add_node(self):
        """
        Function to add a node to the layout.
        :return: None.
        """

        self.layout_right_left.addWidget(self.server_lable)
        self.layout_right_middle.addWidget(self.server_ip)
        self.layout_right_right.addWidget(self.server_port)
        self.update()

    def send_message(self):
        """
        Function to send a message. Write the modified IP-addresses and ports to a txt-file.
        :return: None.
        """

        self.message_button.setDisabled(True)

        for i in range(len(self.notified_server["ip"])):
            if i != "":
                self.notified_server["ip"][i] = self.notified_server_ip[i].text()

        for i in range(len(self.notified_server["port"])):
            if i != "":
                self.notified_server["port"][i] = int(self.notified_server_port[i].text())

        for i in range(len(self.participants_bittorrent["ip"])):
            if i != "":
                self.participants_bittorrent["ip"][i] = self.participants_bittorrent_ip[i].text()

        for i in range(len(self.participants_bittorrent["port"])):
            if i != "":
                self.participants_bittorrent["port"][i] = int(self.participants_bittorrent_port[i].text())

        # refresh txt
        open('notified_server.txt', 'w').write(str(self.notified_server))
        open('participants_bittorrent.txt', 'w').write(str(self.participants_bittorrent))

        self.sender.notified_server = self.notified_server
        self.sender.participants_bittorrent = self.participants_bittorrent

        # send message
        self.sender.connect_send(self.message.text())
        time.sleep(20)
        self.restart_button.setDisabled(False)

    def closeEvent(self, event):
        """
        Function to controll the red x on the main window. Kill all server.
        :param event: event.
        :return: None.
        """

        self.sender.kill()
        event.accept()

    def restart(self):
        """
        Function to restart all server.
        uses: sender.py.
        :return: None.
        """

        self.sender.restart()
        self.message_button.setDisabled(False)
        self.restart_button.setDisabled(True)


app = qw.QApplication(sys.argv)
gui = SenderGui()
gui.show()
app.exec_()
