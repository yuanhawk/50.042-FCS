import math

from prettytable import PrettyTable
from gf2ntemplate import *

# create table for GF(2^4)
n = 16
ip = Polynomial2([1,0,0,1,1])
with open('table1.txt', 'w+') as fout:
    header1 = ['GF(2^4) +']
    header2 = ['GF(2^4) *']

    for i in range(n):
        header1.append(str(i))
        header2.append(str(i))

    t1 = PrettyTable(header1)
    t2 = PrettyTable(header2)

    for j in range(n):
        row_add = [str(j)]
        row_mul = [str(j)]
        for k in range(n):
            row_add.append(GF2N(k).add(GF2N(j)).getInt())
            row_mul.append(GF2N(k, ip=ip).mul(GF2N(j, ip=ip)).getInt())
        t2.add_row(row_mul)
        t1.add_row(row_add)

    print(t1)
    print(t2)

    fout.writelines(str(t1))
