from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto import Random
import base64

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

    def generate_ssh_pair(self) -> None:
        """
        Create pair of SSH keys ciphrated with ECDSA algorithm
        :return: None
        """
        # TODO check if credentials exist in file, if not -- generate pair of keys for further encryption
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

    # TODO redundant?
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
        self.address = "http://127.0.0.1:" + port
