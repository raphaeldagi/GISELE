"""Rodada 39 do diálogo Python <-> Java: o que não é divisor. Bases 5 a 22, até b⁵: nos palíndromos de comprimento 3 e 5 coprimos a
2b, a fração dos divisíveis por cada primo q de {3, 5, 7, 11, 13} que não divide 2b; a correção Π (1 − f_q)/(1 − 1/q); a conta C
(Π p/(p − 1) dos primos de 2b, vezes a correção, sobre ln n, com o log próprio da rodada 26), por comprimento; o medido por
crivo. Rodar da raiz do repositório: python3 dialogo/rodada39.py"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rodada26 import log_  # noqa: E402
from rodada38 import crivo, primos_de  # noqa: E402

BASES = range(5, 23)
QS = (3, 5, 7, 11, 13)


def palindromos(b, L):
    """Os palíndromos de L dígitos na base b, em ordem crescente (primeiro dígito, depois a metade restante)."""
    h = (L + 1) // 2
    for primeiro in range(1, b):
        for resto in range(b ** (h - 1)):
            ds = [primeiro]
            for i in range(h - 2, -1, -1):
                ds.append((resto // b ** i) % b)
            cheio = ds + ds[:L // 2][::-1]
            n = 0
            for d in cheio:
                n = n * b + d
            yield n


def base(b, c):
    """(N coprimos de comprimento 3 e 5, {q: divisíveis}, correção, exatos, medido por L, conta C por L, variância)."""
    ps = primos_de(2 * b)
    f = 1.0
    for p in ps:
        f = f * p / (p - 1)
    qs = [q for q in QS if q not in ps]
    exatos = 0
    for L in (1, 2, 4):
        for n in palindromos(b, L):
            exatos += c[n]
    N = 0
    div = {q: 0 for q in qs}
    for L in (3, 5):
        for n in palindromos(b, L):
            if all(n % p for p in ps):
                N += 1
                for q in qs:
                    div[q] += n % q == 0
    corr = 1.0
    for q in qs:
        corr = corr * (((N - div[q]) * q) / (N * (q - 1)))
    med, conta, var = {}, {}, 0.0
    for L in (3, 5):
        m, s = 0, 0.0
        for n in palindromos(b, L):
            if all(n % p for p in ps):
                m += c[n]
                pr = f * corr / log_(float(n))
                s += pr
                var += pr * (1.0 - pr)
        med[L], conta[L] = m, s
    return N, div, corr, exatos, med, conta, var


def main():
    c = crivo(22 ** 5)
    soma_corr = 0.0
    tot = 0.0
    zs = 0.0
    def5 = deft = 0.0
    for b in BASES:
        N, div, corr, ex, med, conta, var = base(b, c)
        m = ex + med[3] + med[5]
        C = ex + conta[3] + conta[5]
        s = math.sqrt(var)
        soma_corr += abs(corr - 1.0)
        tot += m - C
        if b >= 17:
            zs += (m - C) / s
            def5 += med[5] - conta[5]
            deft += m - C
        print(f"b={b} N={N} div={[div[q] for q in sorted(div)]} correcao={corr.hex()} exatos={ex} medido3={med[3]} medido5={med[5]} "
              f"C3={conta[3].hex()} C5={conta[5].hex()} sigma={s.hex()}")
    print(f"media |correcao-1|={(soma_corr / 18).hex()}; soma medido-C={tot.hex()}; media z 17-22={(zs / 6).hex()}; "
          f"fracao do deficit em L=5={(def5 / deft).hex()}")


if __name__ == "__main__":
    main()
