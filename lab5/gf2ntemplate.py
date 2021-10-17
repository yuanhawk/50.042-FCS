# 50.042 FCS Lab 5 Modular Arithmetics
# Year 2021
import operator
import numpy as np


class Polynomial2:
    def __init__(self, coeffs):
        self.coeff = coeffs
        self.len = len(coeffs)
        self.ops = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.floordiv
        }

    def pad_list(self, p2):
        if self.len < p2.len:
            for i in range(p2.len - self.len):
                self.coeff.append(0)
        elif self.len > p2.len:
            for i in range(self.len - p2.len):
                p2.coeff.append(0)

    def mod(self, val):
        return int(val % 2)

    def xor(self, op_char, val1, val2):
        return self.mod(self.ops[op_char](val1, val2))

    def add(self, p2):
        if self.len < p2.len:
            self.pad_list(p2)
        elif p2.len < self.len:
            p2.pad_list(self)

        p3 = []
        for i in range(len(self.coeff)):
            p3.append(self.xor('+', self.coeff[i], p2.coeff[i]))
        return Polynomial2(p3)

    def sub(self, p2):
        self.pad_list(p2)
        p3 = []
        for i in range(self.len):
            p3.append(self.xor('-', self.coeff[i], p2.coeff[i]))
        return Polynomial2(p3)

    def sub_range(self, p2, start, end):
        count = p2.len - 1
        for i in range(start, end, -1):
            self.coeff[i] = (self.xor('-', self.coeff[i], p2.coeff[count]))
            count -= 1
        return self.coeff

    def mul(self, p2, modp=None):
        max = self.len + p2.len - 1
        # print(max)
        if self.len <= p2.len:
            idx = self.len
            s_arr = self.coeff
            l_arr = p2.coeff
        else:
            idx = p2.len
            l_arr = self.coeff
            s_arr = p2.coeff

        output = []
        for i in range(idx):
            if s_arr[i] == 1:
                intermediate = [0] * i + l_arr + [0] * (max - len(l_arr) - i)
                output.append(intermediate)

        output = np.array(output)
        new_output = []
        calc = np.sum(output, axis=0)
        if isinstance(calc, np.floating):
            new_output.append(self.mod(calc))
        else:
            for i in np.sum(output, axis=0):
                new_output.append(self.mod(i))

        self.coeff = new_output
        if modp:
            if len(new_output) >= modp.len:
                q, r = self.div(modp)
                self.coeff = r
                return r

        return Polynomial2(new_output)

    def div(self, p2):
        q = r = []
        for i in range(len(self.coeff) - 1, p2.len - 2, -1):
            if self.coeff[i] == 1 and i >= p2.len - 1:
                q.append(1)
                r = self.sub_range(p2, start=i, end=i - len(p2.coeff))
            else:
                q.append(0)

        for i in range(len(self.coeff) - 1, -1, -1):
            if r[i] != 0:
                break
            r.pop()

        return Polynomial2(q), Polynomial2(r)

    def __str__(self):
        p = []
        for i in range(self.len - 1, -1, -1):
            if self.coeff[i] == 1:
                if i > 1:
                    p.append(f'x^{i}')
                elif i == 1:
                    p.append('x')
                elif i == 0:
                    p.append('1')
        return '+'.join(p)

    def getInt(self):
        op = ''
        for i in range(self.len - 1, -1, -1):
            op += str(self.coeff[i])
        return int(op, 2)


class GF2N:
    affinemat = [[1, 0, 0, 0, 1, 1, 1, 1],
                 [1, 1, 0, 0, 0, 1, 1, 1],
                 [1, 1, 1, 0, 0, 0, 1, 1],
                 [1, 1, 1, 1, 0, 0, 0, 1],
                 [1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 1, 1, 1, 1, 1, 0, 0],
                 [0, 0, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 1, 1, 1, 1, 1]]
    modt = [1, 1, 0, 0, 0, 1, 1, 0]

    def __init__(self, x, n=8, ip=Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])):
        self.x = bin(x)
        self.coeff = []
        for i in range(len(self.x) - 1, 1, -1):
            self.coeff.append(int(self.x[i]))
        self.poly = Polynomial2(self.coeff)
        self.n = n
        self.ip = ip

    def add(self, g2):
        return self.poly.add(g2.poly)

    def sub(self, g2):
        return self.poly.sub(g2.poly)

    def mul(self, g2):
        return self.poly.mul(g2.poly, self.ip)

    def div(self, g2):
        q, r = self.poly.div(g2.getPolynomial2())
        return GF2N(q.getInt(), self.n, self.ip), GF2N(r.getInt(), self.n, self.ip)

    def getPolynomial2(self):
        return self.poly

    def __str__(self):
        p = []
        for i in range(self.poly.len - 1, -1, -1):
            if self.coeff[i] == 1:
                if i > 1:
                    p.append(f'x^{i}')
                elif i == 1:
                    p.append('x')
                elif i == 0:
                    p.append('1')
        return '+'.join(p)

    def getInt(self):
        return self.poly.getInt()

    # at = 1 mod n
    def mulInv(self):
        # print(self.poly, ' = 101')
        # print(self.ip, ' = 10011')

        q1, r1 = self.ip.div(self.poly)

        q2, r2 = self.poly.div(r1)

        q1q2 = Polynomial2(q1.coeff).mul(Polynomial2(q2.coeff))
        q_x = q1q2.add(Polynomial2([1]))

        return GF2N(q_x.getInt(), self.n, self.ip)

    def pad_list(self, ai, pad):
        for i in range(len(ai)):
            if (len(ai) < pad):
                ai.append(0)
        return ai

    def affineMap(self):
        Ai = GF2N(self.getPolynomial2().getInt()).mulInv()
        Bip = self.pad_list(Ai.coeff, 8)

        map = np.array(self.affinemat)
        Bip = np.dot(map, np.transpose(Bip))
        Bip = np.add(np.transpose(Bip), np.transpose(self.modt))
        Bi = np.mod(np.transpose(Bip), 2)

        return GF2N(Polynomial2(Bi.tolist()).getInt(), self.n, self.ip)


print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')
print('p2=x^3+x^2+1')
p1 = Polynomial2([0, 1, 1, 0, 0, 1])
p2 = Polynomial2([1, 0, 1, 1])
p3 = p1.add(p2)
print('p3= p1+p2 = ', p3)

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')
print('modp=x^8+x^7+x^5+x^4+1')
p4 = Polynomial2([0, 1, 1, 1, 1, 0, 0, 1])
modp = Polynomial2([1, 0, 0, 0, 1, 1, 0, 1, 1])
p5 = p1.mul(p4, modp)
print('p5=p1*p4 mod (modp)=', p5)

print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')
print('p7=x^8+x^4+x^3+x+1')
p6 = Polynomial2([0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1])
p7 = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
p8q, p8r = p6.div(p7)
print('q for p6/p7=', p8q)
print('r for p6/p7=', p8r)

####
print('\nTest 4')
print('======')
g1 = GF2N(100)
g2 = GF2N(5)
print('g1 = ', g1.getPolynomial2())
print('g2 = ', g2.getPolynomial2())
g3 = g1.add(g2)
print('g1+g2 = ', g3)

print('\nTest 5')
print('======')
ip = Polynomial2([1, 1, 0, 0, 1])
print('irreducible polynomial', ip)
g4 = GF2N(0b1101, 4, ip)
g5 = GF2N(0b110, 4, ip)
print('g4 = ', g4.getPolynomial2())
print('g5 = ', g5.getPolynomial2())
g6 = g4.mul(g5)
print('g4 x g5 = ', g6)

print('\nTest 6')
print('======')
g7 = GF2N(0b1000010000100, 13, None)
g8 = GF2N(0b100011011, 13, None)
print('g7 = ', g7.getPolynomial2())
print('g8 = ', g8.getPolynomial2())
q, r = g7.div(g8)
print('g7/g8 =')
print('q = ', q.getPolynomial2())
print('r = ', r.getPolynomial2())

print('\nTest 7')
print('======')
ip = Polynomial2([1, 1, 0, 0, 1])
print('irreducible polynomial', ip)
g9 = GF2N(0b101, 4, ip)
print('g9 = ', g9.getPolynomial2())
print('inverse of g9 =', g9.mulInv().getPolynomial2())


print('\nTest 8')
print('======')
ip = Polynomial2([1, 1, 0, 1, 1, 0, 0, 0, 1])
print('irreducible polynomial', ip)
g10 = GF2N(0xc2, 8, ip)
print('g10 = 0xc2')
g11 = g10.mulInv()
print('inverse of g10 = g11 =', hex(g11.getInt()))
g12 = g11.affineMap()
print('affine map of g11 =', hex(g12.getInt()))
