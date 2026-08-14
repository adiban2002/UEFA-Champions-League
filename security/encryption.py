import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class DataProtector:
    def __init__(self, key: bytes = None):
        self.key = key or AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.key)

    def encrypt_data(self, data: str) -> bytes:
        nonce = os.urandom(12)  
        ciphertext = self.aesgcm.encrypt(nonce, data.encode(), None)
        return nonce + ciphertext

    def decrypt_data(self, encrypted_data: bytes) -> str:
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        decrypted_data = self.aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_data.decode()
