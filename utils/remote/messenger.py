from ecdsa import SigningKey, VerifyingKey


def sign_message(message: str, priv_key: SigningKey) -> str:
    """
    Signs string with private key
    :param message: Text to sign
    :param priv_key: Private key
    :return: Signed message string
    """
    signed_message = priv_key.sign(message.encode())
    return signed_message


def verify_sender(key_list: [], pub_key: str) -> bool:
    """
    Checks if sender is already present on whitelisted connections list
    :param key_list: list of whitelisted senders' public keys
    :param pub_key: current sender's public key
    :return: True if sender's key is present in the array, otherwise false
    """

    return pub_key in key_list


def decode_message(message: str, pub_key: str) -> str:
    """

    :param message:
    :param pub_key:
    :return:
    """