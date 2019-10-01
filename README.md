

************************************START ANONYMOUS NETWORK******************************************

Generate Keys (before the first usage of the anonymous network)
- generate a private and public key -> python3 generateRSAkeys.py (modify the len of the generated keys
and the IP-address just for naming the generated file)
- distribute the public key via scp or other file sharing to all other participant nodes
- save the received public keys in ProofOfConcept/publicKeys

Start the anonymization network on Raspberry Pis
- open and modify node.py -> nano/cat node.py
- change IP address and port if necessary
- to start a server run code in terminal - python3 node.py


Start the anonymization network on Start Sender
- run on your laptop (sender) python3 sender.py
- modify in the Gui the change IP address and ports of all Raspberry Pis
- type message in field
- click on send to send the message to the receiver via the anonymous network
- after the message has reached the receiver - click on the restart button to restart all nodes
- to stopp the anonymous network close the Gui





*********************************INSTALLATION RASPBERRY PI******************************************

Install Raspberry Pi
- Install Debian
- enable SSH via sudo raspi-config

Install pip on Raspberry Pi
- sudo apt-get install python3-pip

Install Cryptodomex on Raspberry Pi
- sudo python3 -m pip install pycryptodomex

Install QT5 on Sender
- pip install PyQt5

Send Files via scp from Laptop to Pi
- scp File.zip pi@address

Connect via ssh from Laptop to Pi
- ssh pi@address

Move file to other directory
- mv -v ~/file.py ~/ProofOfConcept

Delete file
- rm file.py

Delete folder
- rm -r Folder

If you have "key know"-problems while connecting via ssh
- ssh -keyscan -H address >> ~/.ssh/known_hosts
- nano ~/.ssh/known_hosts

Enable usb-media
- sudo apt-get -y install ntfs-3g hfsutils hfsprogs exfat-fuse
- sudo mkdir /media/usbstick
- sudo blkid -o list -w /dev/null
- sudo mount -t ext4 -o defaults /dev/sda /media/usbstick
