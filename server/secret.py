#!/usr/bin/python3

from hashlib import sha256
import secrets
import hmac

def gen_key(*, length: int = 128) -> str:
    return secrets.token_urlsafe(length)

def compare(secret_key: str, request_body: str, request_signature: str) -> bool:
    bsecret_key = secret_key.encode('utf-8')
    brequest_body = request_body.encode('utf-8')
    hmac_obj = hmac.new(bsecret_key, msg=brequest_body, digestmod=sha256)
    generated_hash = "sha256=" + hmac_obj.hexdigest()
    return hmac.compare_digest(generated_hash, request_signature)


def main():
    print(gen_key())

if __name__ == "__main__":
    main()
