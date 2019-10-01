from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP


def generate_keys(address, len_key):
    """
    Function to generate rsa keys.
    :param address: must be string.
    :param len_key: must be int.
    :return: None.
    """

    key = RSA.generate(len_key)
    encrypted_key = key.exportKey(passphrase=None, pkcs=8, protection="scryptAndAES128-CBC")

    # export key to folder
    name_pri = 'privateKeys/private_key_' + address + '.txt'
    name_pub = 'publicKeys/public_key_' + address + '.txt'
    with open(name_pri, 'wb') as f:
        f.write(encrypted_key)
    with open(name_pub, 'wb') as f:
        f.write(key.publickey().exportKey())


# modify here the IP-address (IP-address is just for the name of the file)
# and then len of generated key (1024, 2048, 4096)
generate_keys("192.168.2.108", 1024)

