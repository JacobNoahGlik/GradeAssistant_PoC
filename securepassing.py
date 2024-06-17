import base64
import random

def encur(string):
    return base64.b64encode(
        string.encode('ascii')
    ).decode('ascii')

def decur(string):
    return base64.b64decode(
        string.encode('ascii')
    ).decode('ascii')


def encr(string, no):
    while no > 0:
        string = encur(string)
        no -= 1
    return string

def decr(string, no):
    while no > 0:
        string = decur(string)
        no -= 1
    return string


def update_password(newpass):
    idx = random.randint(9, 28)
    secret = encr(newpass, idx)
    with open('pass.vault', 'w') as pv:
        pv.write(f'{encr(str(idx), 2)}:{secret}')
    return newpass


def safe_logger():
    with open('pass.vault', 'r') as pv:
        p = pv.read()
    idx, secret = p.split(':', 1)
    return update_password(
        decr(secret, int(decr(idx,2)))
    )