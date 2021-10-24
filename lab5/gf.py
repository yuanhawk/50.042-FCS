# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2021
# * Name of Student(s): Tan Li Yuan, Teo Yew Xuan
# * Student ID(s): 1004326, 1004452

def gf_degree(a):
    res = 0
    a >>= 1
    print(a)
    while a != 0:
        a >>= 1
        res += 1
    return res


def gf_invert(a, mod=0x1B):
    v = mod
    g1 = 1
    g2 = 0
    j = gf_degree(a) - 8

    if a == 0:
        return a

    while a != 1:
        if j < 0:

            a, v = v, a
            g1, g2 = g2, g1
            j = -j

        a ^= v << j
        g1 ^= g2 << j

        a %= 256  # Emulating 8-bit overflow
        g1 %= 256  # Emulating 8-bit overflow

        j = gf_degree(a) - gf_degree(v)

    return g1

# print(gf_invert(0xc2))  # 28
