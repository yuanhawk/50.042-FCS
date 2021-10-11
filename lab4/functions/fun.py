# * Name of Student(s): Tan Li Yuan, Teo Yew Xuan
# * Student ID(s): 1004326, 1004452

from constants.pmt import pmt
from constants.sbox import sbox

#takes in 64 bits
def fun(de, mode, m):
    if de == 'e':
        if mode == 'sbox':
            for k, v in sbox.items():
                if m == k:
                    return v
        elif mode == 'pmt':
            for k, v in pmt.items():
                if m == k:
                    return v
    elif de == 'd':
        if mode == 'sbox':
            for k, v in sbox.items():
                if m == v:
                    return k
        elif mode == 'pmt':
            for k, v in pmt.items():
                if m == v:
                    return k
