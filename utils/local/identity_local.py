from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto import Random
from ecdsa import SigningKey, VerifyingKey
import base64
import random

# snippet from https://www.quickprogrammingtips.com/python/aes-256-encryption-and-decryption-in-python.html
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
###


class IdentityLocal:
    def __init__(self):
        self.name = None
        self.address = None
        self.pub_key = None
        self.priv_key = None
        self.salt = None

    def get_ssh_pair(self) -> (str, str):
        try:
            with open(f"keys/{self.name}.pub", "r") as f:
                self.pub_key = VerifyingKey.from_pem(f.read())
            with open(f"keys/{self.name}.priv", "r") as f:
                priv_key_encrypted = f.read()
                priv_key_plain = self.decrypt_key(priv_key_encrypted, "password", self.salt)
                self.priv_key = SigningKey.from_pem(priv_key_plain)
        except OSError:
            print(f"Key pair {self.name}.pub and {self.name}.key not found, generating new pair...")
            self.__generate_ssh_pair()

    def __generate_ssh_pair(self) -> None:
        """
        [PRIVATE METHOD] Create pair of SSH keys ciphrated with ECDSA algorithm
        :return: None
        """
        # TODO check if credentials exist in file, if not -- generate pair of keys for further encryption
        priv_key = SigningKey.generate()
        pub_key = priv_key.verifying_key
        priv_key_encrypted = self.encrypt_key(priv_key.to_pem().decode(), "password", self.salt) # TODO how to store pass and salt? env?
        try:
            with open(f"./keys/{self.name}.pub", "w") as f:
                f.write(pub_key.to_pem().decode())
            with open(f"./keys/{self.name}.priv", "w") as f:
                f.write(priv_key_encrypted.decode())
                print(f"SSH identity created. Files {self.name}.pub and {self.name}.priv were created.")
        except OSError:
            print(
                "Could not write newly generated keys to files. Make sure you have the correct access rights. ",
                "The program will now exit."
            )
            exit(1)
        self.pub_key = pub_key
        self.priv_key = priv_key
        return

    def encrypt_key(self, raw: str, password: str, salt: str) -> bytes:
        """
        Encrypt private key with AES algorithm
        :param raw:
        :param password:
        :param salt:
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
        :param c_text:
        :param password:
        :param salt:
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

        :param password:
        :param salt:
        :return:
        """
        pbkdf2 = PBKDF2(password, salt, 64, 1000)
        key = pbkdf2[:32]
        return key

    def set_node_basic_data(self, node_name, port):
        self.name = node_name
        self.address = "http://127.0.0.1:" + str(port)
        random.seed(node_name)
        self.salt = str(random.random())[2:10].encode()

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
