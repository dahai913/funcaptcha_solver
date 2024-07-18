# import base64
# import hashlib
# import json
# import random
# import string
#
# from Crypto.Cipher import AES


# def aes_encrypt(data, key):
#     pad_len = 16 - (len(data) % 16)
#     padding = chr(pad_len) * pad_len
#     data = data + padding
#     salt = b"".join(random.choice(string.ascii_lowercase).encode() for x in range(8))
#     salted, dx = b"", b""
#     while len(salted) < 48:
#         dx = hashlib.md5(dx + key.encode() + salt).digest()
#         salted += dx
#     key = salted[:32]
#     iv = salted[32:32 + 16]
#     aes = AES.new(key, AES.MODE_CBC, iv)
#     encrypted_data = {"ct": base64.b64encode(aes.encrypt(data.encode())).decode("utf-8"), "iv": iv.hex(),
#                       "s": salt.hex()}
#     return json.dumps(encrypted_data, separators=(',', ':'))
#
#
# def aes_decrypt(data, key):
#     data = json.loads(data)
#     dk = key.encode() + bytes.fromhex(data["s"])
#     md5 = [hashlib.md5(dk).digest()]
#     result = md5[0]
#     for i in range(1, 3 + 1):
#         md5.insert(i, hashlib.md5((md5[i - 1] + dk)).digest())
#         result += md5[i]
#     aes = AES.new(result[:32], AES.MODE_CBC, bytes.fromhex(data["iv"]))
#     decrypted_data = aes.decrypt(base64.b64decode(data["ct"]))
#     pad = decrypted_data[-1]
#     if isinstance(pad, str):
#         pad = ord(pad)
#     decrypted_data = decrypted_data[:-pad]
#     return decrypted_data.decode('utf-8')


import base64
import hashlib
import json
# Form https://github.com/gngpp
import os
import time

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class EncryptionData:
    def __init__(self, ct, iv, s):
        self.ct = ct
        self.iv = iv
        self.s = s


def aes_encrypt(content, password):
    salt = os.urandom(8)
    key, iv = default_evp_kdf(password.encode(), salt)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(content.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    ct_encoded = base64.b64encode(cipher_text).decode('utf-8')

    iv_hex = iv.hex()
    s_hex = salt.hex()

    enc_data = EncryptionData(ct_encoded, iv_hex, s_hex)

    return json.dumps(enc_data.__dict__)


def aes_decrypt(encrypted_content, password):
    enc_data = json.loads(encrypted_content)
    ct = base64.b64decode(enc_data['ct'])
    iv = bytes.fromhex(enc_data['iv'])
    s = bytes.fromhex(enc_data['s'])

    key, _ = default_evp_kdf(password.encode(), s)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ct) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted_data.decode('utf-8')


def evp_kdf(password, salt, key_size=32, iv_size=16, iterations=1, hash_algorithm='md5'):
    if hash_algorithm.lower() != 'md5':
        raise ValueError("Unsupported hash algorithm")

    derived_key_bytes = b""
    block = b""

    while len(derived_key_bytes) < (key_size + iv_size):
        hasher = hashlib.md5()
        hasher.update(block + password + salt)
        block = hasher.digest()

        for _ in range(1, iterations):
            hasher = hashlib.md5()
            hasher.update(block)
            block = hasher.digest()

        derived_key_bytes += block

    return derived_key_bytes[:key_size], derived_key_bytes[key_size:key_size + iv_size]


def default_evp_kdf(password, salt):
    return evp_kdf(password, salt)

