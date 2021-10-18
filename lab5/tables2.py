from prettytable import PrettyTable
from gf2ntemplate import *

# create table for GF(2^4)
n = 16
with open('table2.txt', 'w+') as fout:
    header = ['']

    for i in range(n):
        header.append(hex(i)[2:])

    t = PrettyTable(header)
    for j in range(n):
        row_aff = [hex(j)[2:]]
        for k in range(n):
            ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
            hexa = f'0x{hex(j)[2:]}{hex(k)[2:]}'
            g10 = GF2N(int(hexa, 16), 8, ip)
            row_aff.append(hex(g10.mulInv().affineMap().getInt()))
        t.add_row(row_aff)
    print(t)

    fout.writelines(str(t))
