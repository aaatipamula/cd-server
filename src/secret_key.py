import hashlib
import secrets
import hmac
import os

def gen_key(*, length: int = 256):
    return secrets.token_urlsafe(length)

def compare(client_key, server_hash):
    client_hash ="sha256=" + hmac.new(client_key, digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(client_hash, server_hash)

