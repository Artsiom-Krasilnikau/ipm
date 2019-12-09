import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import dct, idct
from skimage import io
from skimage.util import view_as_blocks
from os.path import dirname

u1, v1 = 4, 5
u2, v2 = 5, 4
N = 8
P = 25


def increment(x):
    is_positive = x >= 0
    if is_positive:
        return x+1
    else:
        return x-1


def decrement(x):
    is_less_than_one = x <= 1 and x >= -1
    is_positive = x >= 0
    if is_less_than_one:
        return 0
    elif is_positive:
        return x - 1
    else:
        return x + 1


def get_delta_coefficients(transform):
    delta = np.abs(transform[u1, v1]) - np.abs(transform[u2, v2])
    return delta


def is_valid(transform, bit, threshold):
    delta = get_delta_coefficients(transform)
    if (bit == 0) and (delta > threshold):
        return True
    elif (bit == 1) and (delta < -threshold):
        return True
    return False


def modify_coefficients(transform, bit):
    coefficients = transform.copy()
    if bit == 0:
        coefficients[u1, v1] = increment(coefficients[u1, v1])
        coefficients[u2, v2] = decrement(coefficients[u2, v2])
    elif bit == 1:
        coefficients[u1, v1] = decrement(coefficients[u1, v1])
        coefficients[u2, v2] = increment(coefficients[u2, v2])
    return coefficients


def insert_bit(block, bit):
    patch = block.copy()
    coefficients = dct(dct(patch, axis=0, norm='ortho'), axis=1, norm='ortho')
    while not is_valid(coefficients, bit, P) or (bit != take_bit(patch)):
        coefficients = modify_coefficients(coefficients, bit)
        patch = double_to_byte(
            idct(idct(coefficients, axis=0, norm='ortho'), axis=1, norm='ortho'))
    return patch


def insert_message(original, msg):
    new_image = original.copy()
    blue = new_image[:, :, 2]
    blocks = view_as_blocks(blue, block_shape=(N, N))
    h = blocks.shape[1]
    for index, bit in enumerate(msg):
        i = index // h
        j = index % h
        block = blocks[i, j]
        i_index = i*N
        j_index = j*N
        blue[i_index: i_index + N, j_index: j_index +
             N] = insert_bit(block, bit)
    new_image[:, :, 2] = blue
    return new_image


def take_bit(block):
    transform = dct(dct(block, axis=0), axis=1)
    delta = get_delta_coefficients(transform)
    if delta > 0:
        return 0
    else:
        return 1


def retrieve_message(image, length):
    blocks = view_as_blocks(image[:, :, 2], block_shape=(N, N))
    h = blocks.shape[1]
    return [take_bit(blocks[index // h, index % h]) for index in range(length)]


def double_to_byte(arr):
    return np.uint8(np.round(np.clip(arr, 0, 255)))


def get_bits(message):
    result = []
    for symbol in message:
        bits = format(ord(symbol), '0>8b')
        for bit in bits:
            result.append(int(bit))
    return result


def get_message(bits):
    result = []
    bit_length = len(bits)
    for index in range(0, bit_length, 8):
        byte_block = bits[index:index+8]
        byte_value = 0
        for index, bit in enumerate(reversed(byte_block)):
            if bit == 1:
                byte_value += 2**index
        result.append(chr(byte_value))
    return ''.join(result)


if __name__ == '__main__':
    pwd = '{}/'.format(dirname(__file__))
    path_to_image = pwd + 'funny_dog.jpg'

    original = io.imread(path_to_image)

    message = input('Type message: ')
    bit_message = get_bits(message)
    new_image = insert_message(original, bit_message)
    bit_message_from_image = retrieve_message(new_image, len(bit_message))
    message_from_image = get_message(bit_message_from_image)

    print('Message:', message)
    print('Message from image:', message_from_image)
    print('Messages are equal?:', 'Yes' if message ==
          message_from_image else 'No')

    io.imshow(np.hstack((original, new_image)))
    plt.show()
