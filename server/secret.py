#!/usr/bin/python3

from hashlib import sha256, pbkdf2_hmac
from getpass import getpass
import secrets
import hmac
import sys
import os

def hash_password(password: str, salt_length: int = 16, iterations: int = 100000) -> str:
    salt = os.urandom(salt_length)
    hashed = pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    return f"{salt.hex()}:{hashed.hex()}:{iterations}"

def verify_password(stored_password: str, provided_password: str) -> bool:
    salt, stored_hash, iterations = stored_password.split(':')
    new_hash = pbkdf2_hmac('sha256', provided_password.encode(), bytes.fromhex(salt), int(iterations))
    return hmac.compare_digest(stored_hash, new_hash.hex())

def gen_key(*, length: int = 32) -> str:
    return secrets.token_urlsafe(length)

def compare(secret_key: str, request_body: str, request_signature: str) -> bool:
    bsecret_key = secret_key.encode('utf-8')
    brequest_body = request_body.encode('utf-8')
    hmac_obj = hmac.new(bsecret_key, msg=brequest_body, digestmod=sha256)
    generated_hash = "sha256=" + hmac_obj.hexdigest()
    return hmac.compare_digest(generated_hash, request_signature)

def main():
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else ""

    if not arg: return

    if arg == "genkey":
        print(gen_key())
    elif arg == "passwd":
        passwd = getpass()
        print(hash_password(passwd))

if __name__ == "__main__":
    main()
