import sys
from hashlib import md5
from os import urandom
from os.path import dirname

parent_dir = dirname(dirname(__file__))
sys.path.append(parent_dir)
from shared.elliptic_curve import Curve, mod_invert


MODE_SIZE = 32

CURVE_PARAMS = (
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97,
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD94,
    0x00000000000000000000000000000000000000000000000000000000000000a6,
)


def sign(curve, q, point, private_key, digest):
    e = int.from_bytes(digest, 'big') % q
    if e == 0:
        e = 1
    while True:
        k = int.from_bytes(urandom(MODE_SIZE), 'big') % q
        if k == 0:
            continue

        r, _ = curve.scalar_multiply(k, point)
        r %= q
        if r == 0:
            continue

        d = private_key * r
        k *= e
        s = (d + k) % q
        if s == 0:
            continue

        return s.to_bytes(MODE_SIZE, 'big') + r.to_bytes(MODE_SIZE, 'big')


def verify(curve, q, point, signature, public, digest):
    p = curve.p
    s = int.from_bytes(signature[:MODE_SIZE], 'big')
    r = int.from_bytes(signature[MODE_SIZE:], 'big')
    if not 0 < r < q or not 0 < s < q:
        return False

    e = int.from_bytes(digest, 'big') % q
    if e == 0:
        e = 1
    v = mod_invert(e, q)
    z1 = s * v % q
    z2 = q - r * v % q
    p1x, p1y = curve.scalar_multiply(z1, point)
    q1x, q1y = curve.scalar_multiply(z2, (public[0], public[1]))

    delta_x = p1x - q1x
    m = (p1y - q1y) * mod_invert(delta_x, p)
    x_c = (m ** 2 - p1x - q1x) % p
    if x_c < 0:
        x_c += p

    R = x_c % q
    return R == r


def get_pulic(curve, value, point):
    return curve.scalar_multiply(value, point)


def get_private(limit):
    key = int.from_bytes(urandom(32), 'big')
    while key >= limit:
        key = int.from_bytes(urandom(32), 'big')
    return key


if __name__ == '__main__':
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
    
    print("Signature is verified", is_verified)
