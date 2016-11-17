from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Crypto import Random
from base64 import b64encode, b64decode, urlsafe_b64encode
import os

"""
This module basically exists to provide some security for when RouteWatch supports external DBs, allowing the secure
storage of access credentials in an "untrusted" location.
At the time of writing the cryptography library used defaults to AES-CBC-128 with HMAC-SHA256 authentication and is
widely believed to be a cryptographically secure implementation.
"""


def get_secret():
    """
    Finds or creates a new secret for use with the encrypt and decrypt functions.
    :return:
    :rtype: bytes
    """
    with open("master.key", "ba+") as f:
        # Checks the size of the secret and loads it if it's valid
        if os.path.getsize("master.key") != 32: # If it's not the correct length it generates a new one and stores it.
            f.seek(0)
            r = Random.new()
            secret = r.read(32)
            f.write(secret)
        else:
            f.seek(0)
            secret = f.read(32)
    return secret


def encrypt(data, secret):
    """
    Basically wraps the cryptography lib to reduce code duplication
    :param data:
    :type data: bytes
    :param secret:
    :type secret: bytes
    :return:
    :rtype: bytes, str
    """
    # Generate a cryptographically secure salt
    r = Random.new()
    salt = r.read(16)
    # Generates a suitable key from the secret by HMACing it with the salt
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000,backend=default_backend())
    key = urlsafe_b64encode(kdf.derive(secret))
    # Encrypts the data
    f = Fernet(key)
    ciphertext = f.encrypt(data)
    return b64encode(salt+ciphertext)


def decrypt(encodedciphertext, secret):
    """
    Basically wraps the cryptography lib to reduce code duplication
    :param encodedciphertext:
    :type encodedciphertext: bytes
    :param secret:
    :type secret: bytes
    :return:
    """
    # Split out the salt from the ciphertext
    ciphertext = b64decode(encodedciphertext)
    salt = ciphertext[:16]
    ciphertext = ciphertext[16:]
    # Regenerates the key by HMACing the secret with the salt
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000,backend=default_backend())
    key = urlsafe_b64encode(kdf.derive(secret))
    # Decrypts the data
    f = Fernet(key)
    data = f.decrypt(ciphertext)
    return data
