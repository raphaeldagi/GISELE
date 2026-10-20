"""Rodada 87 do diálogo Python <-> Java (Parte 121): a regressão logística do experimento do ÂNGULO DUPLO do NEXUS–RAPHAEL 2.2.0, bit a bit.
Os dados vêm de um LCG inteiro: u em [−1, 1) faz o papel de cos θ, e o atributo do ângulo duplo é 2u² − 1 (a identidade cos 2θ = 2cos²θ − 1,
sem chamar cos); y = 1 se u² > 0,49. Duas logísticas por descida do gradiente (taxa 0,8, 300 passos, como no arquivo): só com u, e com
(u, 2u² − 1). A sigmoide usa o exp PRÓPRIO (dialogo/exatas.py). Da raiz: python3 dialogo/rodada87.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

N, PASSOS, TAXA, SEMENTE = 200, 300, 0.8, 1210


def dados():
    x = SEMENTE
    out = []
    for _ in range(N):
        x = (1103515245 * x + 12345) % 2147483648
        u = (x / 2147483648.0) * 2.0 - 1.0
        out.append((u, 2.0 * u * u - 1.0, 1 if u * u > 0.49 else 0))
    return out


def sigmoide(z):
    if z >= 0.0:
        return 1.0 / (1.0 + exp_(-z))
    e = exp_(z)
    return e / (1.0 + e)


def treinar(com_duplo):
    d = dados()
    w = [0.0, 0.0, 0.0]
    for _ in range(PASSOS):
        g = [0.0, 0.0, 0.0]
        for u, c2, y in d:
            z = w[0] + w[1] * u + (w[2] * c2 if com_duplo else 0.0)
            r = sigmoide(z) - y
            g[0] += r
            g[1] += r * u
            if com_duplo:
                g[2] += r * c2
        for i in range(3):
            w[i] = w[i] - TAXA * (g[i] / N)
    brier = 0.0
    for u, c2, y in d:
        p = sigmoide(w[0] + w[1] * u + (w[2] * c2 if com_duplo else 0.0))
        brier += (p - y) * (p - y)
    return w, brier / N


def main():
    for com in (False, True):
        w, b = treinar(com)
        print(("duplo " if com else "simples ") + " ".join(v.hex() for v in w) + " brier " + b.hex())
    print("fim")


if __name__ == "__main__":
    main()
