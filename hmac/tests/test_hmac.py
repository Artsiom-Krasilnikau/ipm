import pytest
import sys
print(sys.path)
import hashlib
from hmac.hmac import hmac


def test_hmac():
    key = b'SuperKey'
    message = b'Hello World'
    digest = hmac(key, message, hashlib.md5)
    assert digest == b'\xa0\xd3\xd7\xd5(w\xa3\xce\xb9\xfaRR\xa8\x1a\xfcb'

