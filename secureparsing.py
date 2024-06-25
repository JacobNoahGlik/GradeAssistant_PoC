import package_manager

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import hashlib
import random
import secrets
import time
import os
from presets import InvalidUsageError



class EncryptionMethods:
    @staticmethod
    def encrypt(plaintext, password):
        key = EncryptionMethods.generate_key(password)
        iv = secrets.token_bytes(16)
        encryptor = EncryptionMethods._generate_cipher_context(key,
                                                               iv).encryptor()
        padded_data = EncryptionMethods._padd(plaintext)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + encrypted_data).decode()

    @staticmethod
    def decrypt(ciphertext, password):
        key = EncryptionMethods.generate_key(password)
        decoded_ciphertext = base64.b64decode(ciphertext)
        iv = decoded_ciphertext[:16]
        ciphertext = decoded_ciphertext[16:]
        cipher = EncryptionMethods._generate_cipher_context(key, iv)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = EncryptionMethods._unpadd(decrypted_data)
        return plaintext.decode()

    @staticmethod
    def hash_string(input_string):
        hash_object = hashlib.sha256()
        hash_object.update(input_string.encode())
        hashed_string = hash_object.hexdigest()
        return hashed_string

    @staticmethod
    def _generate_cipher_context(key, iv):
        return Cipher(algorithms.AES(key),
                      modes.CBC(iv),
                      backend=default_backend())

    @staticmethod
    def _padd(plaintext):
        padder = padding.PKCS7(128).padder()
        return padder.update(plaintext.encode()) + padder.finalize()

    @staticmethod
    def _unpadd(padded_data):
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()

    @staticmethod
    def generate_key(password):
        return hashlib.sha256(password.encode()).digest()



class TimmingSystem:
    @staticmethod
    def current_time() -> float:
        return time.time()

    @staticmethod
    def cuttoff(time: float) -> tuple[int, int]:
        return (int(time / 10), int((time / 10) - 1))



class Obfuscator:
    @staticmethod
    def encur(string):
        return base64.b64encode(string.encode('ascii')).decode('ascii')

    @staticmethod
    def decur(string):
        return base64.b64decode(string.encode('ascii')).decode('ascii')

    @staticmethod
    def encr(string, no):
        while no > 0:
            string = Obfuscator.encur(string)
            no -= 1
        return string

    @staticmethod
    def decr(string, no):
        while no > 0:
            string = Obfuscator.decur(string)
            no -= 1
        return string



class SecureStorage:
    @staticmethod
    def save(file_name: str, data: str):
        time, _ = TimmingSystem.cuttoff(TimmingSystem.current_time())
        password = EncryptionMethods.hash_string(f'password:{time}')
        cyphertext = EncryptionMethods.encrypt(data, password)
        with open(file_name, 'w') as f:
            f.write(cyphertext)

    @staticmethod
    def load(file_name: str):
        time, time_backup = TimmingSystem.cuttoff(
            SecureStorage._get_file_time(file_name))
        with open(file_name, 'r') as f:
            cyphertext = f.read()
        try:
            password = EncryptionMethods.hash_string(f'password:{time}')
            plaintext = EncryptionMethods.decrypt(cyphertext, password)
        except Exception as e:
            print(f'\nException has ocured: {e.__repr__()}')
            password = EncryptionMethods.hash_string(f'password:{time_backup}')
            plaintext = EncryptionMethods.decrypt(cyphertext, password)
        return plaintext

    @staticmethod
    def _get_file_time(file: str):
        file_statistics = os.stat(file)
        return file_statistics.st_mtime



class SecureParsing:
    @staticmethod
    def update_password(newpass):
        idx = random.randint(9, 28)
        secret = Obfuscator.encr(newpass, idx)
        SecureStorage.save('token.vault',
                           f'{Obfuscator.encr(str(idx), 2)}:{secret}')
        return newpass

    @staticmethod
    def safe_logger():
        stream = SecureStorage.load('token.vault')
        idx, secret = stream.split(':', 1)
        return SecureParsing.update_password(
            Obfuscator.decr(secret, int(Obfuscator.decr(idx, 2))))



class ReplicateTokenNotSetError(Exception):
    pass



if not os.path.exists('token.vault'):
    raise ReplicateTokenNotSetError('Could not find "token.vault" file. Update your replicate token by running "python3 update.py --show-all"')



if __name__ == "__main__":
    raise InvalidUsageError("This file should not be run. Only import this file and its contents. Do not run this file directly.")
