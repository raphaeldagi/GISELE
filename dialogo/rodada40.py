"""Rodada 40 do diálogo Python <-> Java: o endereço da falta. Base 21, palíndromos de 5 dígitos coprimos a 42: por primeiro dígito
d₀ e por dígito do meio d₂, o medido (crivo) contra a conta C da rodada 39 reescalada para o total medido; o qui-quadrado de cada
classificação. E as bases 23 a 28 com a conta C: o z de cada uma. Rodar da raiz do repositório: python3 dialogo/rodada40.py"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rodada26 import log_  # noqa: E402
from rodada38 import crivo, primos_de  # noqa: E402
from rodada39 import base, palindromos  # noqa: E402


def classes(b, c):
    """{'d0': {d: [medido, conta, var]}, 'd2': {...}} nos palíndromos de 5 dígitos coprimos a 2b."""
    ps = primos_de(2 * b)
    f = 1.0
    for p in ps:
        f = f * p / (p - 1)
    corr = base(b, c)[2]
    out = {"d0": {}, "d2": {}}
    for n in palindromos(b, 5):
        if not all(n % p for p in ps):
            continue
        pr = f * corr / log_(float(n))
        for nome, d in (("d0", n // b ** 4), ("d2", (n // (b * b)) % b)):
            x = out[nome].setdefault(d, [0, 0.0, 0.0])
            x[0] += c[n]
            x[1] += pr
            x[2] += pr * (1.0 - pr)
    return out


def qui(cl):
    """(qui-quadrado com a conta reescalada para o total medido, graus de liberdade, k)."""
    m = 0
    e = 0.0
    for d in sorted(cl):
        m += cl[d][0]
        e += cl[d][1]
    k = m / e
    q = 0.0
    for d in sorted(cl):
        mc, ec, vc = cl[d]
        q += (mc - k * ec) * (mc - k * ec) / (k * vc)
    return q, len(cl) - 1, k


def main():
    c = crivo(28 ** 5)
    cl = classes(21, c)
    for nome in ("d0", "d2"):
        for d in sorted(cl[nome]):
            mc, ec, vc = cl[nome][d]
            print(f"{nome}={d} medido={mc} conta={ec.hex()}")
        q, gl, k = qui(cl[nome])
        print(f"{nome}: qui2={q.hex()} gl={gl} k={k.hex()} qui2/gl={(q / gl).hex()}")
    zs = 0.0
    neg = 0
    for b in range(23, 29):
        N, div, corr, ex, med, conta, var = base(b, c)
        m = ex + med[3] + med[5]
        C = ex + conta[3] + conta[5]
        s = math.sqrt(var)
        z = (m - C) / s
        zs += z
        neg += z < 0
        print(f"b={b} medido={m} C={C.hex()} sigma={s.hex()} z={z.hex()}")
    print(f"media z 23-28={(zs / 6).hex()}; negativos={neg}")


if __name__ == "__main__":
    main()
