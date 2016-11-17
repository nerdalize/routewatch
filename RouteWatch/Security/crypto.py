from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from Crypto import Random
from base64 import b64encode, b64decode, urlsafe_b64encode
import os


def get_secret():
    with open("master.key", "ba+") as f:
        if os.path.getsize("master.key") != 32:
            f.seek(0)
            r = Random.new()
            secret = r.read(32)
            f.write(secret)
        else:
            f.seek(0)
            secret = f.read(32)
    return secret


def encrypt(data, secret):
    r = Random.new()
    salt = r.read(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000,backend=default_backend())
    key = urlsafe_b64encode(kdf.derive(secret))
    f = Fernet(key)
    ciphertext = f.encrypt(data)
    return b64encode(salt+ciphertext)


def decrypt(encodedciphertext, secret):
    ciphertext = b64decode(encodedciphertext)
    salt = ciphertext[:16]
    ciphertext = ciphertext[16:]
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000,backend=default_backend())
    key = urlsafe_b64encode(kdf.derive(secret))
    f = Fernet(key)
    data = f.decrypt(ciphertext)
    return data
