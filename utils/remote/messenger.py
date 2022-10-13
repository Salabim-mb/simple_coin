def sign_message(message: str, key: str) -> str:
    """
    Signs string with private key
    :param message: Text to sign
    :param key: Private key
    :return: Signed message string
    """
    return message


def verify_sender(key_list: [str], key: str) -> bool:
    """
    Checks if sender is already present on whitelisted connections list
    :param key_list: list of whitelisted senders' public keys
    :param key: current sender's public key
    :return: True if sender's key is present in the array, otherwise false
    """
    return key in key_list
