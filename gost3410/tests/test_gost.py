import pytest
from hashlib import md5
from gost3410.gost3410 import Curve, CURVE_PARAMS, get_private, get_pulic, sign, verify

def test_gost():
    curve = Curve(*CURVE_PARAMS)
    q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6C611070995AD10045841B09B761B893
    point = (1, 0x8D91E471E0989CDA27DF505A453F2B7635294F2DDF23E3B122ACC99C9E9F1E14)
    message = b"Do you remember funny dog?"

    private_key = get_private(q)
    public_key = get_pulic(curve, private_key, point)

    signature = sign(curve, q, point,
                     private_key,
                     md5(message).digest())
    is_verified = verify(curve, q, point,
                         signature, public_key,
                         md5(message).digest())
    assert is_verified
