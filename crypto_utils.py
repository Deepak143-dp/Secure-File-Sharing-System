from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16

def encrypt_file(data, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data, BLOCK_SIZE))

def decrypt_file(data, key):
    iv = data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(data[16:]), BLOCK_SIZE)
