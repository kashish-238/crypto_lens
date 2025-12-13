import base64
import json
import os
from dataclasses import dataclass

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


DEFAULT_ITERATIONS = 390_000  # strong default (PBKDF2-HMAC-SHA256)


def _derive_fernet_key(password: str, salt: bytes, iterations: int) -> bytes:
    if not password:
        raise ValueError("Password is required.")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    key = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(key)  # Fernet expects urlsafe base64 key


def encrypt_message(message: str, password: str, iterations: int = DEFAULT_ITERATIONS) -> dict:
    if not message:
        raise ValueError("Message is required.")

    salt = os.urandom(16)
    fernet_key = _derive_fernet_key(password=password, salt=salt, iterations=iterations)
    token = Fernet(fernet_key).encrypt(message.encode("utf-8"))

    return {
        "v": 1,
        "kdf": "pbkdf2-sha256",
        "it": int(iterations),
        "s": base64.urlsafe_b64encode(salt).decode("utf-8"),
        "t": token.decode("utf-8"),
    }


def decrypt_message(payload: dict, password: str) -> str:
    try:
        salt = base64.urlsafe_b64decode(payload["s"].encode("utf-8"))
        iterations = int(payload["it"])
        token = payload["t"].encode("utf-8")
    except Exception as e:
        raise ValueError("Invalid encrypted payload format.") from e

    fernet_key = _derive_fernet_key(password=password, salt=salt, iterations=iterations)

    try:
        plaintext = Fernet(fernet_key).decrypt(token)
        return plaintext.decode("utf-8")
    except InvalidToken as e:
        raise ValueError("Wrong password or corrupted encrypted text.") from e


def pack_payload_for_url(payload: dict) -> str:
    """
    Makes the payload URL-safe in a single query param.
    """
    raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8")


def unpack_payload_from_url(packed: str) -> dict:
    raw = base64.urlsafe_b64decode(packed.encode("utf-8"))
    return json.loads(raw.decode("utf-8"))
