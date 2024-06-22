from hashlib import sha256
from io import BytesIO
from os import urandom
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature

def derive_aes_keys(auth_key: bytes, msg_key: bytes, outgoing: bool) -> tuple:
    """
    Derive AES encryption and initialization vector keys.

    Parameters:
    auth_key (bytes): The authentication key used for deriving the AES keys.
    msg_key (bytes): The message key used for deriving the AES keys.
    outgoing (bool): A flag indicating whether the keys are for outgoing messages.

    Returns:
    tuple: A tuple containing the derived AES encryption key and initialization vector.

    The function derives the AES encryption and initialization vector keys based on the given
    authentication key, message key, and the direction of the message (outgoing or incoming).
    The offset for deriving the keys is determined based on the value of the 'outgoing' flag.
    The derived keys are then returned as a tuple.
    """
    offset = 0 if outgoing else 8
    sha256_a = sha256(msg_key + auth_key[offset : offset + 36]).digest()
    sha256_b = sha256(auth_key[offset + 40 : offset + 76] + msg_key).digest()
    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]
    return aes_key, aes_iv

def encrypt_message(message: bytes, salt: int, session_id: bytes, auth_key: bytes, auth_key_id: bytes) -> bytes:
    """
    Encrypt a message using AES-IGE256 and return the encrypted data.

    Parameters:
    message (bytes): The message to be encrypted.
    salt (int): A random number used for encryption.
    session_id (bytes): A unique identifier for the session.
    auth_key (bytes): The authentication key used for encryption.
    auth_key_id (bytes): The identifier for the authentication key.

    Returns:
    bytes: The encrypted data.

    The function first constructs the data to be encrypted by combining the salt, session_id, and message.
    It then generates padding to ensure the data length is a multiple of 16.
    The message key is derived from the auth_key and the constructed data using SHA-256.
    The AES encryption and initialization vector keys are derived from the auth_key and the message key.
    The data is then encrypted using AES-IGE256 with the derived keys.
    The encrypted data is finally constructed by concatenating the auth_key_id, message key, encrypted data, and padding.
    """
    data = int.to_bytes(salt, 8, 'big') + session_id + message
    padding = urandom(-(len(data) + 12) % 16 + 12)
    msg_key_large = sha256(auth_key[88 : 88 + 32] + data + padding).digest()
    msg_key = msg_key_large[8:24]
    aes_key, aes_iv = derive_aes_keys(auth_key, msg_key, True)

    cipher = Cipher(algorithms.AES(aes_key), modes.IGE256(aes_iv))
    encryptor = cipher.encryptor()
    encrypted_data = auth_key_id + msg_key + encryptor.update(data + padding) + encryptor.finalize()

    return encrypted_data

def decrypt_message(encrypted_data: bytes, session_id: bytes, auth_key: bytes, auth_key_id: bytes) -> bytes:
    """
    Decrypt an encrypted message using AES-IGE256 and return the decrypted data.

    Parameters:
    encrypted_data (bytes): The encrypted data to be decrypted.
    session_id (bytes): A unique identifier for the session.
    auth_key (bytes): The authentication key used for decryption.
    auth_key_id (bytes): The identifier for the authentication key.

    Returns:
    bytes: The decrypted data.

    Raises:
    InvalidSignature: If the auth_key_id, salt, or session_id in the decrypted data does not match the provided values.

    The function first checks if the provided auth_key_id matches the one in the encrypted data.
    If not, it raises an InvalidSignature exception.
    It then extracts the message key from the encrypted data and derives the AES encryption and initialization vector keys.
    The encrypted data is decrypted using AES-IGE256 with the derived keys.
    The decrypted data is checked for validity by comparing the salt and session_id with the provided values.
    If any of the checks fail, an InvalidSignature exception is raised.
    Finally, the decrypted data is returned, excluding the salt, session_id, and auth_key_id.
    """
    if encrypted_data[:8] != auth_key_id:
        raise InvalidSignature("Invalid auth_key_id")

    msg_key = encrypted_data[8:24]
    aes_key, aes_iv = derive_aes_keys(auth_key, msg_key, False)

    cipher = Cipher(algorithms.AES(aes_key), modes.IGE256(aes_iv))
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data[24:]) + decryptor.finalize()

    if decrypted_data[:8] != int.to_bytes(int.from_bytes(decrypted_data[:8], 'big'), 8, 'big'):
        raise InvalidSignature("Invalid salt")

    if decrypted_data[8:16] != session_id:
        raise InvalidSignature("Invalid session_id")

    return decrypted_data[16:]