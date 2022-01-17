import random
from primePy import primes
import math
import hashlib
import ast


class PGP:
    """
    Implementation of PGP Protocol
    """
    @staticmethod
    def random_large_prime():
        """
        Generates a random large prime number
        """
        while True:
            prime_num = random.randint(2, 10)
            if primes.check(prime_num) is True:
                return prime_num

    @staticmethod
    def relative_prime(prime_num):
        """
        Generates a relative prime number from a prime number
        """
        while True:
            relative_prime = random.randint(2, 10)
            if math.gcd(relative_prime, prime_num) == 1:
                return relative_prime

    @staticmethod
    def calc_d(e, z):
        while True:
            d = random.randint(2, 100)
            product = e * d
            if e != d:
                if product % z == 1:
                    return d

    @staticmethod
    def rsa(secret_key=False):
        """
        Sets up the PGP protocol by generating prime numbers
        """
        p = PGP.random_large_prime()
        q = PGP.random_large_prime()
        n = p * q
        z = (p-1) * (q-1)
        e = PGP.relative_prime(z)
        d = PGP.calc_d(e, z)
        if not secret_key:
            return [n, e, d]
        else:
            return [n, d]

    @staticmethod
    def data_to_integer(data):
        str_data = str(data)
        bytes_data = str_data.encode('utf-8')
        #print("byte data: " + str(bytes_data))
        hex_data = bytes_data.hex()
        #print("hex data: " + str(hex_data))
        integer_data = int(hex_data, 16)
        #print("Passed in: " + str(integer_data))
        return integer_data

    @staticmethod
    def public_key(n, e, data):
        """
        Returns the data encrypted with a public key
        """
        integer_data = PGP.data_to_integer(data)
        print("Public: " + str(integer_data))
        print("n: " + str(n) + " e: " + str(e))
        encrypted_data = (integer_data ** e) % n
        print(encrypted_data)
        return encrypted_data       #c

    @staticmethod
    def integer_to_data(integer_data):
        #print("Passed in: " + str(integer_data))
        hex_data = (hex(integer_data)[2:])
        #print("hex data: " + str(hex_data))
        bytes_data = bytes.fromhex(hex_data)
        #print("byte data: " + str(bytes_data))
        data = bytes_data.decode('utf-8')
        return data

    @staticmethod
    def private_key(n, d, encrypted_data):
        """
        Return the decrypted data
        """
        print("n: " + str(n) + " d: " + str(d))
        data = (encrypted_data ** d) % n
        print(data)
        unencrypted_data = PGP.integer_to_data(data)
        return unencrypted_data             #m

    @staticmethod
    def pgp_sender(data, server_n, server_e, client_n, client_d):
        """

        """
        secret_key = PGP.rsa(secret_key=True)
        encoded_data = data.encode()
        hashed_data = hashlib.sha1(encoded_data)
        hashed_data_str = hashed_data.hexdigest()
        encrypted_hash_message = PGP.public_key(secret_key[0], secret_key[1], hashed_data_str)
        secret_key_str = str(secret_key)
        encrypted_secret_key = PGP.public_key(server_n, server_e, secret_key_str)
        digital_signature = PGP.public_key(client_n, client_d, data)
        #print("Digital Signature: " + str(digital_signature))
        return [encrypted_hash_message, encrypted_secret_key, digital_signature]

    @staticmethod
    def pgp_receiver(all_data, client_n, client_e, server_n, server_d):
        """

        """
        data = PGP.private_key(client_n, client_e, all_data[2])
        #print(data)
        secret_key_str = PGP.private_key(server_n, server_d, all_data[1])
        #print(secret_key_str)
        secret_key = ast.literal_eval(secret_key_str)
        hash_message = PGP.private_key(secret_key[0], secret_key[1], all_data[0])
        data_2 = data
        tmp_hash_message = hashlib.sha1(data_2)
        if tmp_hash_message == hash_message:
            print(data)
        else:
            print("Error! The data has been tampered with!")


pgp = PGP()
#server_keys = pgp.rsa()
#client_keys = pgp.rsa()
server_keys = [35, 5, 29]
client_keys = [35, 5, 29]
#print(server_keys)
#print(client_keys)
message = "h"
#print(pgp.data_to_integer(message))
data = pgp.pgp_sender(message, server_keys[0], server_keys[1], client_keys[0], client_keys[2])
pgp.pgp_receiver(data, client_keys[0], client_keys[1], server_keys[0], server_keys[2])



