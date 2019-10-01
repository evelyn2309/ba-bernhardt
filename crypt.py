from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from random import choice
import string
from Cryptodome.Util.Padding import pad, unpad


class Crypt(object):

    def __init__(self):
        self.block_size = 128

    def encrypt_message_rsa(self, message, address):
        """
        Function to encrypt a message via rsa.
        Uses: RSA from Pycrytodome.PublicKEY and PKCS1_OAEP from Cryptodome.Cipher, pad and unpad Cryptodome.Util.Padding.
        :param address: must be string.
        :param message: must be string.
        :return: cipher.
        """

        # print("Encrypt message " + str(message) + " via RSA.")
        name_pub = 'publicKeys/public_key_' + address + '.txt'
        recipient_key = RSA.import_key(open(name_pub).read())
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        return cipher_rsa.encrypt(message.encode('utf8').strip())


    def decrypt_message_rsa(self, cipher, address):
        """
        Function to decrypt a message via rsa.
        Uses: RSA from Pycrytodome.PublicKEY and PKCS1_OAEP from Cryptodome.Cipher, pad and unpad Cryptodome.Util.Padding.
        :param address:
        :param cipher: must be string.
        :return: decrypted message.
        """

        try:
            # print("Decrypt message " + str(cipher) + " via RSA.")
            name_pri = 'privateKeys/private_key_' + address + '.txt'
            priv_key = RSA.import_key(open(name_pri).read())
            decipher_rsa = PKCS1_OAEP.new(priv_key)
            de = decipher_rsa.decrypt(cipher)
            return de.decode('utf8')
        except Exception as e:
            print(e)
            print("Wrong key - you are not the receiver!")


    def encrypt_message_aes(self, message, session_key):
        """
        Function to encrypt a message via aes.
        Uses: AES and PKCS1_OAEP from Cryptodome.Cipher, pad and unpad Cryptodome.Util.Padding.
        :param message: must be string or bytes.
        :param session_key: must be string.
        :return: cipher.
        """

        # print("Encrypt message " + str(message) + " via AES with the " + session_key + ".")
        if type(message) == bytes:
            cipher = AES.new(session_key.encode('utf8'), AES.MODE_ECB).encrypt(pad(message, self.block_size))
        else:
            cipher = AES.new(session_key.encode('utf8'), AES.MODE_ECB).encrypt(
                pad(message.encode('utf8'), self.block_size))
        return cipher


    def decrypt_message_aes(self, cipher, session_key):
        """
        Function to encrypt a message via rsa.
        Uses: AES and PKCS1_OAEP from Cryptodome.Cipher, pad and unpad Cryptodome.Util.Padding.
        :param cipher: must be string or bytes.
        :param session_key: must be string.
        :return: decrypted message.
        """

        try:
            # print("Decrypt message " + str(cipher) + " via AES with the " + session_key + ".")
            c = AES.new(session_key.encode('utf8'), AES.MODE_ECB).decrypt(cipher)
            if type(c) == bytes:
                decipher = unpad(c, self.block_size)
            else:
                decipher = unpad(c, self.block_size).decode('utf8')
            return decipher
        except Exception as e:
            print(e)
            print("Wrong key - you are not the receiver!")


    def generate_session_key(self, session_key='', size=16):
        """Function to generate session keys.
        Input Arguments: session_key: string default '', size: int default 16.
        Uses: Random.choice.
        Returns: session_key
        """
        if size > 0:
            session_key += choice(string.ascii_letters)
            return self.generate_session_key(session_key, size - 1)
        return session_key


    def evaluate_package(self, package: bytes, address):
        """
        Function to evaluate the given package.
        :param address:
        :param package: must be bytes.
        :return: (next_node, message, package_next, session_key_dec).
        """
        print("unpack and evaluate the received package...")
        package_decode = eval(package.decode('utf8'))
        session_key_dec = self.decrypt_message_rsa(package_decode["enc_key"], address)
        package_decrypt = eval(self.decrypt_message_aes(package_decode["enc_package"], session_key_dec).decode('utf8'))
        message = ""
        next_node = ""
        package_next = ""
        if "message" in package_decrypt:
            message = package_decrypt["message"]
        if "next" in package_decrypt:
            next_node = package_decrypt["next"]
        if "package" in package_decrypt:
            package_next = package_decrypt["package"].encode('utf8')
        return next_node, message, package_next, session_key_dec
