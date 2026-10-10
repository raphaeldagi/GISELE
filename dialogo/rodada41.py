"""Rodada 41 do diálogo Python <-> Java: tendência ou dispersão. O z = (medido − C)/σ dos primos palíndromos (conta C da rodada 39)
nas bases 5 a 40; a reta de mínimos quadrados de z contra b nas 36 bases, e a média e o desvio-padrão dos z das bases novas (35 a 40).
Rodar da raiz do repositório: python3 dialogo/rodada41.py"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rodada38 import crivo  # noqa: E402
from rodada39 import base  # noqa: E402


def zs(bases, c):
    saida = []
    for b in bases:
        N, div, corr, ex, med, conta, var = base(b, c)
        m = ex + med[3] + med[5]
        C = ex + conta[3] + conta[5]
        saida.append((b, m, (m - C) / math.sqrt(var)))
    return saida


def reta(pontos):
    """(inclinação, intercepto, erro-padrão da inclinação) de z contra b, em laços."""
    n = len(pontos)
    sb = sz = 0.0
    for b, z in pontos:
        sb += b
        sz += z
    mb, mz = sb / n, sz / n
    sbb = sbz = 0.0
    for b, z in pontos:
        sbb += (b - mb) * (b - mb)
        sbz += (b - mb) * (z - mz)
    beta = sbz / sbb
    alfa = mz - beta * mb
    rr = 0.0
    for b, z in pontos:
        r = z - (alfa + beta * b)
        rr += r * r
    return beta, alfa, math.sqrt(rr / (n - 2)) / math.sqrt(sbb)


def media_dp(v):
    n = len(v)
    s = 0.0
    for x in v:
        s += x
    m = s / n
    q = 0.0
    for x in v:
        q += (x - m) * (x - m)
    return m, math.sqrt(q / (n - 1))


def main():
    c = crivo(40 ** 5)
    todos = zs(range(5, 41), c)
    for b, m, z in todos:
        print(f"b={b} medido={m} z={z.hex()}")
    beta, alfa, ep = reta([(float(b), z) for b, m, z in todos])
    m, dp = media_dp([z for b, _, z in todos if b >= 35])
    mt, dpt = media_dp([z for b, _, z in todos])
    print(f"reta: inclinacao={beta.hex()} intercepto={alfa.hex()} ep={ep.hex()}")
    print(f"bases 35-40: media={m.hex()} dp={dp.hex()}; todas: media={mt.hex()} dp={dpt.hex()}")


if __name__ == "__main__":
    main()
