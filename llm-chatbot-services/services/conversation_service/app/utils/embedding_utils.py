import hashlib


def mock_embedding(text: str) -> list[float]:
    hash_bytes = hashlib.sha256(text.encode()).digest()
    return [b / 255 for b in hash_bytes[:128]]
