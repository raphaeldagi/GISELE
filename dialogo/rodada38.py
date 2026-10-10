"""Rodada 38 do diálogo Python <-> Java: o fator do dígito final nos primos palíndromos. Para cada base b de 5 a 16, até b⁵: os
primos palíndromos (crivo), a conta A (2/ln n nos palíndromos ímpares de comprimento ímpar ≥ 3, mais os exatos de 1 e 2+ pares) e
a conta B (Π p/(p − 1) dos primos p | 2b, nos palíndromos coprimos a 2b, sobre ln n), com o desvio σ da conta B. O logaritmo é o
próprio da rodada 26 (log_), para os bits serem os mesmos. Rodar da raiz do repositório: python3 dialogo/rodada38.py"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rodada26 import log_  # noqa: E402

BASES = range(5, 17)


def primos_de(m):
    ps, p = [], 2
    while p * p <= m:
        if m % p == 0:
            ps.append(p)
            while m % p == 0:
                m //= p
        p += 1
    if m > 1:
        ps.append(m)
    return ps


def crivo(n):
    c = bytearray([1]) * n
    c[0] = c[1] = 0
    i = 2
    while i * i < n:
        if c[i]:
            c[i * i::i] = bytearray(len(range(i * i, n, i)))
        i += 1
    return c


def base(b, c):
    """(medido, conta A, conta B, variância da conta B)."""
    ate = b ** 5
    ps = primos_de(2 * b)
    f = 1.0
    for p in ps:
        f = f * p / (p - 1)
    medido = 0
    exatos = 0
    A = B = var = 0.0
    for n in range(1, ate):
        ds, x = [], n
        while x:
            x, r = divmod(x, b)
            ds.append(r)
        if ds != ds[::-1]:
            continue
        medido += c[n]
        L = len(ds)
        if L == 1 or L % 2 == 0:
            exatos += c[n]
            continue
        ln = log_(float(n))
        if n % 2:
            A += 2.0 / ln
        if all(n % p for p in ps):
            q = f / ln
            B += q
            var += q * (1.0 - q)
    return medido, A + exatos, B + exatos, var


def main():
    c = crivo(16 ** 5)
    tm = 0
    tb = 0.0
    perto = 0
    absrel = 0.0
    for b in BASES:
        m, a, bb, var = base(b, c)
        s = math.sqrt(var)
        perto += abs(m - bb) < 2.0 * s
        absrel += abs(m - bb) / bb
        tm += m
        tb += bb
        print(f"b={b} medido={m} contaA={a.hex()} contaB={bb.hex()} sigma={s.hex()}")
    print(f"bases a menos de 2 sigma={perto}; media |medido-B|/B={(absrel / 12).hex()}; soma medido-B={(tm - tb).hex()}")


if __name__ == "__main__":
    main()
