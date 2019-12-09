CURVE_PARAMS = (
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97,
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD94,
    0x00000000000000000000000000000000000000000000000000000000000000a6,
)


def mod_invert(a, n):
    """
    # k^-1 = p - (-k)^-1 mod p
    """

    if a < 0:
        return n - mod_invert(-a, n)
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r:
        quotinent = r // new_r
        t, new_t = new_t, t - quotinent * new_t
        r, new_r = new_r, r - quotinent * new_r
    if r > 1:
        return -1
    if t < 0:
        t += n
    return t


class Curve:
    SIZE = 32

    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

    def _pos(self, v):
        if v < 0:
            return v + self.p
        return v

    def _add(self, p1x, p1y, p2x, p2y):
        if p1x == p2x and p1y == p2y:
            t = ((3 * p1x * p1x + self.a) * mod_invert(2 * p1y, self.p)) % self.p
        else:
            tx = self._pos(p2x - p1x) % self.p
            ty = self._pos(p2y - p1y) % self.p
            t = (ty * mod_invert(tx, self.p)) % self.p
        tx = self._pos(t * t - p1x - p2x) % self.p
        ty = self._pos(t * (p1x - tx) - p1y) % self.p
        return tx, ty

    def scalar_multiply(self, degree, point):
        x, y = point
        tx, ty = x, y
        degree -= 1
        if not degree:
            raise ValueError("Degree error")

        while degree:
            if degree & 1:
                tx, ty = self._add(tx, ty, x, y)
            degree = degree >> 1
            x, y = self._add(x, y, x, y)
        return tx, ty
