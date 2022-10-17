from ecdsa import SigningKey, VerifyingKey
import requests


def sign_message(message: str, priv_key: SigningKey) -> str:
    """
    Signs string with private key
    :param message: Text to sign
    :param priv_key: Private key
    :return: Signed message string
    """
    signature = priv_key.sign(message.encode()).decode()
    return signature


def verify_sender(key_list: [], pub_key: str) -> bool:
    """
    Checks if sender is already present on whitelisted connections list
    :param key_list: list of whitelisted senders' public keys
    :param pub_key: current sender's public key
    :return: True if sender's key is present in the array, otherwise false
    """

    return len(list(filter(lambda x: x['pub_key'] == pub_key, key_list))) > 0


def check_if_message_authentic(message: str, signature: str, key: str) -> bool:
    """
    Check if message sent is authored by specified host
    :param message: String that needs authentication
    :param signature: Digital signature of a message
    :param key: public_key to check with
    :return: True if message is coming from specified sender
    """
    vk = VerifyingKey.from_pem(key)
    return vk.verify(signature, message)