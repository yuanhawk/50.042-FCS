#!/usr/bin/env python3

# Present skeleton file for 50.042 FCS
from functions.fun import fun
from collections import OrderedDict

# constants
FULLROUND = 31

# Rotate left: 0b1001 --> 0b0011

def rol(val, r_bits, max_bits): return \
    (val << r_bits % max_bits) & (2 ** max_bits - 1) | \
    ((val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))


# Rotate right: 0b1001 --> 0b1100


def ror(val, r_bits, max_bits): return \
    ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | \
    (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))


def get_hex_wo_0x(hex_int):
    return hex(hex_int[2:])

def get_hex_from_str(hex_string):
    return int(hex_string, 16)

def get_hex_int(hex_string):
    return int(hex_string, 16)


def get_bin_wo_0b(bin_int):
    return bin(bin_int[2:])


def get_bin_int(bin_string):
    return int(bin_string, 2)

def pad_hex(hexa, padding):
    return hex(hexa)[2:].zfill(padding)

def pad_binary(binary, padding):
    # e.g.0b100 -> 0b00100  pad_binary(Ob100,2)
    return bin(binary)[2:].zfill(padding)


def genRoundKeys(key):
    keys_dict = {0: 32}

    new_key = key

    for i in range(1, FULLROUND + 2):
        keys_dict[i] = new_key >> 16

        # rotate right of 61 bits
        sushi = pad_binary(ror(new_key, 19, 80), 80)

        # sbox on k79-76
        slayer = sKeyLayer(sushi)

        # ^ round counter
        new_key = int(xLayer(i, slayer), 2)
    return keys_dict


def sKeyLayer(sushi):
    hexa = fun('e', 'sbox', hex(int(sushi[:4], 2)))
    b = pad_binary(int(hexa, 16), 4) + sushi[4:]
    return b


def xLayer(lsb, slayer):
    xlayer = slayer[:60]
    xlayer += str(pad_binary(addRoundKey(int(slayer[60:65], 2), lsb), 5))
    xlayer += slayer[65:]
    return xlayer


def addRoundKey(state, Ki):
    return state ^ Ki

# 64 bits -> 4 bits per space
def sBoxLayer(state, mode, bits):
    #1 hexa char is 4 bits
    state = pad_hex(state, int(bits/4))
    state_op = ''

    for i in state:
        index = fun(mode, 'sbox', '0x' + i)
        state_op += (index[2])

    return int(hex(get_hex_int(state_op)), 16)


def pLayer(state, mode):
    state_dict = {}
    new_state = list(pad_binary(state, 64))
    for idx, val in enumerate(new_state):
        state_dict[fun(mode, 'pmt', idx)] = val

    out = ''
    for v in OrderedDict(sorted(state_dict.items())).values():
        out += v
    return int(out, 2)


def present_round(state, roundKey):
    new_state = addRoundKey(state, roundKey)
    new_state = sBoxLayer(new_state, 'e', 64)
    new_state = pLayer(new_state, 'e')
    return new_state


def present_inv_round(state, roundKey):
    new_state = pLayer(state, 'd')
    new_state = sBoxLayer(new_state, 'd', 64)
    new_state = addRoundKey(new_state, roundKey)
    return new_state


def present(plain, key):
    K = genRoundKeys(key)
    state = plain
    for i in range(1, FULLROUND + 1):
        state = present_round(state, K[i])
    state = addRoundKey(state, K[32])
    return state


def present_inv(cipher, key):
    K = genRoundKeys(key)
    state = cipher
    state = addRoundKey(state, K[32])
    for i in range(FULLROUND, 0, -1):
        state = present_inv_round(state, K[i])
    return state


if __name__ == "__main__":
    # Testvector for key schedule
    key1 = 0x00000000000000000000
    keys = genRoundKeys(key1)
    keysTest = {0: 32, 1: 0, 2: 13835058055282163712, 3: 5764633911313301505, 4: 6917540022807691265,
                5: 12682149744835821666, 6: 10376317730742599722, 7: 442003720503347, 8: 11529390968771969115,
                9: 14988212656689645132, 10: 3459180129660437124, 11: 16147979721148203861, 12: 17296668118696855021,
                13: 9227134571072480414, 14: 4618353464114686070, 15: 8183717834812044671, 16: 1198465691292819143,
                17: 2366045755749583272, 18: 13941741584329639728, 19: 14494474964360714113, 20: 7646225019617799193,
                21: 13645358504996018922, 22: 554074333738726254, 23: 4786096007684651070, 24: 4741631033305121237,
                25: 17717416268623621775, 26: 3100551030501750445, 27: 9708113044954383277, 28: 10149619148849421687,
                29: 2165863751534438555, 30: 15021127369453955789, 31: 10061738721142127305, 32: 7902464346767349504}
    for k in keysTest.keys():
        assert keysTest[k] == keys[k]

    # Testvectors for single rounds without keyscheduling
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    round1 = present_round(plain1, key1)
    round11 = 0xffffffff00000000
    assert round1 == round11

    round2 = present_round(round1, key1)
    round22 = 0xff00ffff000000
    assert round2 == round22

    round3 = present_round(round2, key1)
    round33 = 0xcc3fcc3f33c00000
    assert round3 == round33

    # invert single rounds
    plain11 = present_inv_round(round1, key1)
    assert plain1 == plain11
    plain22 = present_inv_round(round2, key1)
    assert round1 == plain22
    plain33 = present_inv_round(round3, key1)
    assert round2 == plain33

    # Everything together
    plain1 = 0x0000000000000000
    key1 = 0x00000000000000000000
    cipher1 = present(plain1, key1)
    plain11 = present_inv(cipher1, key1)
    assert plain1 == plain11

    plain2 = 0x0000000000000000
    key2 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher2 = present(plain2, key2)
    plain22 = present_inv(cipher2, key2)
    assert plain2 == plain22

    plain3 = 0xFFFFFFFFFFFFFFFF
    key3 = 0x00000000000000000000
    cipher3 = present(plain3, key3)
    plain33 = present_inv(cipher3, key3)
    assert plain3 == plain33

    plain4 = 0xFFFFFFFFFFFFFFFF
    key4 = 0xFFFFFFFFFFFFFFFFFFFF
    cipher4 = present(plain4, key4)
    plain44 = present_inv(cipher4, key4)
    assert plain4 == plain44
