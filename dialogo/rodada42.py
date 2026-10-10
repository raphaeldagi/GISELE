"""Rodada 42 do diálogo Python <-> Java: a densidade que a conta usa. Para cada base b de 5 a 40: R_b = π(b⁵)/(Li(b⁵) − Li(2)), com Li pela
série Li(x) = γ + ln ln x + Σ_{k ≥ 1} (ln x)^k/(k·k!) (log próprio da rodada 26); a conta C da rodada 39 multiplicada por R_b (σ por √R_b); e a
inclinação de z contra b, antes e depois. Rodar da raiz do repositório: python3 dialogo/rodada42.py"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rodada26 import log_  # noqa: E402
from rodada38 import crivo  # noqa: E402
from rodada39 import base  # noqa: E402
from rodada41 import reta  # noqa: E402

GAMA = 0.5772156649015329


def li(x):
    L = log_(float(x))
    s = 0.0
    termo = 1.0
    for k in range(1, 200):
        termo = termo * L / k  # L^k/k!
        s += termo / k
        if termo / k < 1e-17 * s:
            break
    return GAMA + log_(L) + s


def main():
    c = crivo(40 ** 5)
    li2 = li(2)
    antes, depois = [], []
    maior = 0.0
    for b in range(5, 41):
        x = b ** 5
        pi = c[:x].count(1)
        R = pi / (li(x) - li2)
        if b >= 10:
            maior = max(maior, abs(R - 1.0))
        N, div, corr, ex, med, conta, var = base(b, c)
        m = ex + med[3] + med[5]
        C = ex + conta[3] + conta[5]
        s = math.sqrt(var)
        C2 = ex + (conta[3] + conta[5]) * R
        s2 = s * math.sqrt(R)
        antes.append((float(b), (m - C) / s))
        depois.append((float(b), (m - C2) / s2))
        print(f"b={b} pi={pi} R={R.hex()} z={((m - C) / s).hex()} z2={((m - C2) / s2).hex()}")
    b1 = reta(antes)[0]
    b2 = reta(depois)[0]
    print(f"maior |R-1| (10-40)={maior.hex()}; inclinacao antes={b1.hex()} depois={b2.hex()} mudanca={abs(b2 - b1).hex()}")


if __name__ == "__main__":
    main()
