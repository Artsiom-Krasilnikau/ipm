import pytest
from dh.dh import get_public, get_private, curve


def test_dh():
    a = 192841
    b = 742728
    G = (132864, 81275427)

    public_a = get_public(curve, a, G)
    public_b = get_public(curve, b, G)

    private_a = get_private(curve, a, public_b)
    private_b = get_private(curve, b, public_a)
    assert private_a == private_b == 1090534863938014915337073139192401738053648927303979415145294071239340123395
