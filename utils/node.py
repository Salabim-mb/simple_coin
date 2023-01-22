from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto import Random
from ecdsa import SigningKey, VerifyingKey
import base64
import random
import requests
from utils.message_generator import MessageGenerator
from utils.blockchain import Blockchain
from utils.miner import Miner
from utils.wallet.Transaction import Transaction
from utils.wallet.Wallet import Wallet
from utils.block import Block
import json

# snippet from https://www.quickprogrammingtips.com/python/aes-256-encryption-and-decryption-in-python.html
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
###
LOCAL_ADDRESS = "http://127.0.0.1"
searchable_port_suf = range(5001, 5003)     # Port range to search addresses


class Node:
    def __init__(self, node_name, port):
        self.name = node_name
        self.address = "http://127.0.0.1:" + str(port)
        self.node_list: [] = []
        self.transaction_pool: [] = []
        random.seed(node_name)
        self.salt = str(random.random())[2:10].encode()
        self.pub_key, self.priv_key = self.get_ssh_pair()
        self.orphan_list: [Block] = []

        self.register_node_in_blockchain(self.get_data_to_send())

        self.wallet = Wallet(self)
        self.blockchain = Blockchain(self)
        self.blockchain.fetch_blocks()

        self.message_generator = MessageGenerator(self)
        self.miner = Miner(self)

    def get_ssh_pair(self):
        """
        Read a pair of public and private key from files
        :return:
        """
        try:
            with open(f"keys/{self.name}.pub", "r") as f:
                pub_key = VerifyingKey.from_pem(f.read())
            with open(f"keys/{self.name}.priv", "r") as f:
                priv_key_encrypted = f.read()
                priv_key_plain = self.decrypt_key(priv_key_encrypted, "password", self.salt)
                priv_key = SigningKey.from_pem(priv_key_plain)
            return pub_key, priv_key
        except OSError:
            print(f"Key pair {self.name}.pub and {self.name}.key not found, generating new pair...")
            return self.__generate_ssh_pair()

    def __generate_ssh_pair(self):
        """
        [PRIVATE METHOD] Create pair of SSH keys ciphrated with ECDSA algorithm
        :return: None
        """
        priv_key = SigningKey.generate()
        pub_key = priv_key.verifying_key
        priv_key_encrypted = self.encrypt_key(priv_key.to_pem().decode(), "password", self.salt) # TODO how to store pass and salt? env?
        try:
            with open(f"./keys/{self.name}.pub", "w") as f:
                f.write(pub_key.to_pem().decode())
            with open(f"./keys/{self.name}.priv", "w") as f:
                f.write(priv_key_encrypted.decode())
                print(f"SSH identity created. Files {self.name}.pub and {self.name}.priv were created.")
        except OSError as e:
            print(
                "Could not write newly generated keys to files. Make sure you have the correct access rights. ",
                "The program will now exit.",
                str(e)
            )
            exit(1)
        return pub_key, priv_key

    def encrypt_key(self, raw: str, password: str, salt: str) -> bytes:
        """
        Encrypt private key with AES algorithm
        :param raw: raw string to encrypt
        :param password: super duper secret string that is a base for AES algorithm
        :param salt: random string based on a node name
        :return: Ciphertext with SSH key
        """
        private_key = self.get_key(password, salt)
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8')))

    def decrypt_key(self, c_text: str, password: str, salt: str) -> str:
        """
        Decrypt private key with AES algorithm
        :param c_text: ciphertext containing private key
        :param password: super duper secret string that is a base for AES algorithm
        :param salt: random string based on a node name
        :return: Plaintext with SSH key
        """
        private_key = self.get_key(password, salt)
        enc = base64.b64decode(c_text)
        iv = enc[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))

    @staticmethod
    def get_key(password, salt) -> (int, bytes):
        """

        :param password: base for PBKDF2 algorithm hash
        :param salt: random string based on a node name
        :return: Tuple containing key to encrypt with AES
        """
        pbkdf2 = PBKDF2(password, salt, 64, 1000)
        key = pbkdf2[:32]
        return key

    def get_data_to_send(self) -> {}:
        """
        Serializes data for JSON-valid response
        :return: Object with data
        """
        return {
            'name': self.name,
            'address': self.address,
            'pub_key': base64.b64encode(self.pub_key.to_string()).decode()
        }

    def print_node_list(self) -> None:
        """
        Prints list of nodes in blockchain
        :return:
        """
        print("Current node list:", self.node_list)

    def register_node_in_blockchain(self, item: {} = None) -> None:
        """
        Add new node to blockchain and broadcast updated list of nodes to other nodes to let them update it too
        :param item: Node to append and broadcast through network
        :return:
        """
        if item is not None:
            self.node_list.append(item)
        for port in searchable_port_suf:
            host = f"{LOCAL_ADDRESS}:{port}"
            if host == item['address']:
                continue
            try:
                response = requests.post(url=(host + "/register-node"), json=self.node_list)
                self.node_list = response.json()
            except Exception as e:
                print(f"Error with node {host}, couldn't find active target host. {str(e)}")

    def filter_transaction_pool(self, transaction_pool_received):
        """
        Verify if received block contains local transaction and remove duplicates as they are already
        added to blockchain
        :param transaction_pool_received:
        :return:
        """
        for transaction in json.loads(transaction_pool_received):
            for index, local_transaction in enumerate(self.transaction_pool):
                if transaction["id"] == local_transaction["id"]:
                    self.transaction_pool.remove(index)
