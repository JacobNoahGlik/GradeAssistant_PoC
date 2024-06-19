import base64
import random
from util import InvalidUsageError



class SecureData:
    @staticmethod
    def encur(string):
        return base64.b64encode(
            string.encode('ascii')
        ).decode('ascii')

    @staticmethod
    def decur(string):
        return base64.b64decode(
            string.encode('ascii')
        ).decode('ascii')

    @staticmethod
    def encr(string, no):
        while no > 0:
            string = SecureData.encur(string)
            no -= 1
        return string

    @staticmethod
    def decr(string, no):
        while no > 0:
            string = SecureData.decur(string)
            no -= 1
        return string

    @staticmethod
    def update_password(newpass):
        idx = random.randint(9, 28)
        secret = SecureData.encr(newpass, idx)
        with open('pass.vault', 'w') as pv:
            pv.write(f'{SecureData.encr(str(idx), 2)}:{secret}')
        return newpass

    @staticmethod
    def safe_logger():
        with open('pass.vault', 'r') as pv:
            p = pv.read()
        idx, secret = p.split(':', 1)
        return SecureData.update_password(
            SecureData.decr(secret, int(SecureData.decr(idx,2)))
        )



if __name__ == "__main__":
    raise InvalidUsageError("This file should not be run. Only import this file and its contents. Do not run this file directly.")
