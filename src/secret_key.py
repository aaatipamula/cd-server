#!/usr/bin/python3

from hashlib import sha256
import secrets
import hmac

def gen_key(*, length: int = 128) -> str:
    return secrets.token_urlsafe(length)

def compare(client_key: bytes, msg: str, server_hash: str) -> bool:
    client_hash ="sha256=" + hmac.new(client_key, msg, digestmod=sha256).hexdigest()
    return hmac.compare_digest(client_hash, server_hash)

def export_key() -> str:
    SECRET_KEY = gen_key()
    print(SECRET_KEY)
    return SECRET_KEY

if __name__ == "__main__":
    export_key()
