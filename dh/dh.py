import sys
from os.path import dirname

parent_dir = dirname(dirname(__file__))
sys.path.append(parent_dir)

from shared.elliptic_curve import Curve, CURVE_PARAMS
curve = Curve(*CURVE_PARAMS)

def get_public(curve, private_number, G):
    return curve.scalar_multiply(private_number, G)

def get_private(curev, private_number, public_number):
    return curve.scalar_multiply(private_number, public_number)[0]


if __name__ == '__main__':
    a = 192841
    b = 742728
    G = (132864, 81275427)

    public_a = get_public(curve, a, G)
    public_b = get_public(curve, b, G)

    private_a = get_private(curve, a, public_b)
    private_b = get_private(curve, b, public_a)
    assert private_a == private_b
    print(f"Shared private key:", private_a)
