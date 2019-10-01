import hashlib


class Hashing(object):
    def __init__(self):
        pass

    @staticmethod
    def hash_message(message):
        """
        Function to hash a message.
        Uses: hashlib.
        :param message: must be string.
        :return: hash_value.
        """

        if type(message) == bytes:
            hash_value = hashlib.sha256(message).hexdigest()
        else:
            hash_value = hashlib.sha256(message.encode('utf-8')).hexdigest()
        # print("Message " + str(message) + " has been hashed.")
        return hash_value

    @staticmethod
    def check_hash(hash_value, message):
        """
        Function to check if the given hash value belongs to the given message.
        :param hash_value: bytes.
        :param message: string or bytes.
        :return: True/ False.
        """

        if type(message) == bytes:
            if hash_value == hashlib.sha256(message).hexdigest():
                # print("The given hash " + hash_value + " corresponds with the message " + str(message) + ".")
                return True
            else:
                # print("The given hash " + hash_value + " did not correspond with the message " + str(message) + ".")
                return False
        else:
            if hash_value == hashlib.sha256(message.encode('utf-8')).hexdigest():
                # print("The given hash " + hash_value + " corresponds with the message " + message + ".")
                return True
            else:
                # print("The given hash " + hash_value + " did not correnspond with the message " + message + ".")
                return False
