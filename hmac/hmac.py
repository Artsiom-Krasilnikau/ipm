def hmac(key, message, digest):
    opad = bytes((x ^ 0x5C) for x in range(256))
    ipad = bytes((x ^ 0x36) for x in range(256))

    inner = digest()
    outer = digest()

    block_size = inner.block_size

    if len(key) > block_size:
        key = digest(key).digest()
    key = key.ljust(block_size, b'\0')

    outer.update(key.translate(opad))
    inner.update(key.translate(ipad))
    inner.update(message)
    outer.update(inner.digest())

    return outer.digest()
