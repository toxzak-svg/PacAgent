
import time
from backpack.crypto import derive_key
from unittest.mock import patch

def test_speed():
    start = time.time()
    derive_key("password")
    print(f"Original time: {time.time() - start:.4f}s")

    with patch("backpack.crypto.PBKDF2HMAC") as mock_kdf:
        # We need to make sure the mock behaves enough like the real thing if needed,
        # but derive_key just calls kdf.derive().
        # Actually, derive_key instantiates PBKDF2HMAC.
        # So we mock the class.
        mock_instance = mock_kdf.return_value
        mock_instance.derive.return_value = b"x" * 32 # 32 bytes key
        
        start = time.time()
        derive_key("password")
        print(f"Mocked time: {time.time() - start:.4f}s")

if __name__ == "__main__":
    test_speed()
