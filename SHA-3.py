# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 15:42:53 2024

@author: Servies_PC
"""
# Constants for SHA-3
RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808a, 0x8000000080008000,
    0x000000000000808b, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009,
    0x000000000000008a, 0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
    0x000000008000808b, 0x800000000000008b, 0x8000000000008089, 0x8000000000008003,
    0x8000000000008002, 0x8000000000000080, 0x000000000000800a, 0x800000008000000a,
    0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008
]

# Rotate left operation
def rotl(x, n):
    #return (x << n) | (x >> (64 - n))
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF


# Keccak-f permutation
def keccak_f(state):
    for rnd in range(24):
        state = keccak_round(state, RC[rnd])
    return state

# One round of the Keccak-f permutation
def keccak_round(state, round_constant):
    # Theta step
    C = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20] for x in range(5)]
    D = [C[(x + 4) % 5] ^ rotl(C[(x + 1) % 5], 1) for x in range(25)]
    # print("Length of D: ", len(D))
    # print("Values of D: ", D)
    # print("Length of State: ", len(state))
    # print("Values of State: ", state)
    state = [state[x] ^ D[x] for x in range(25)]

    # Rho and pi steps
    x, y = 1, 0
    current = state[x + 5 * y]
    for t in range(24):
        x, y = y, (2 * x + 3 * y) % 5
        current, state[x + 5 * y] = state[x + 5 * y], rotl(current, (t + 1) * (t + 2) // 2 % 64)

    # Chi step
    for y in range(5):
        T = [state[x + 5 * y] for x in range(5)]
        for x in range(5):
            state[x + 5 * y] ^= (~T[(x + 1) % 5]) & T[(x + 2) % 5]

    # Iota step
    state[0] ^= round_constant

    return state

# Padding function for SHA-3
def pad_message(message, block_size):
    message += b'\x06'
    padding_length = block_size - (len(message) % block_size) - 1
    message += bytes([0] * padding_length)
    message += b'\x80'
    return message

# def pad_message(message, block_size):
#     message += b'\x06'
#     print(len(message))
#     message += bytes([0] * (block_size - len(message) % block_size - 1))
#     message += b'\x80'
#     print(len(message))
#     return message

def sha3(message, hash_size):
    # Keccak-p permutations for different hash sizes
    if hash_size == 224:
        rate = 1152
        capacity = 448
    elif hash_size == 256:
        rate = 1088
        capacity = 512
    elif hash_size == 384:
        rate = 832
        capacity = 768
    elif hash_size == 512:
        rate = 576
        capacity = 1024
    else:
        raise ValueError("Unsupported hash size")

    block_size = rate // 8
    message = pad_message(message, block_size)
    state = [0] * 25

    for i in range(0, len(message), block_size):
        block = message[i:i + block_size]
        for j in range(len(block) // 8):
            state[j] ^= int.from_bytes(block[j * 8:(j + 1) * 8], byteorder='big')
        state = keccak_f(state)

    # Convert state to bytes
    hash_bytes = b""
    for num in state:
        hash_bytes += num.to_bytes(8, byteorder='big')

    return hash_bytes[:hash_size // 8]

if __name__ == "__main__":
    # Example:
    data = b"Hello, world!"
    hashed_data = sha3(data, 256)
    hashed_data_bytes = bytes(bytearray(x % 256 for x in hashed_data))
    print("SHA-3 hash:", hashed_data_bytes.hex())