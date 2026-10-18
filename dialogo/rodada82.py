"""Rodada 82 do diálogo Python <-> Java (Parte 115): as DEZ CAMADAS CONTRAPOSTAS (pesos a, 1/a, a, ... com a = 2), tanh pelo exp PRÓPRIO,
frente e trás: o gradiente de ponta a ponta ∂h₁₀/∂h₀ e os DEZ gradientes sobrepostos ∂h₁₀/∂w_k. Bit a bit.
Da raiz: python3 dialogo/rodada82.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

N, A, H0 = 10, 2.0, 0.5


def tanh_(x):
    e = exp_(2.0 * x)
    return (e - 1.0) / (e + 1.0)


def cadeia():
    w = [A if k % 2 == 0 else 1.0 / A for k in range(N)]
    hs = [H0]
    for k in range(N):
        hs.append(tanh_(w[k] * hs[k]))
    g = 1.0
    gw = [0.0] * N
    for k in range(N - 1, -1, -1):
        d = 1.0 - hs[k + 1] * hs[k + 1]
        gw[k] = g * d * hs[k]
        g = g * d * w[k]
    return hs[N], g, gw


def main():
    h, g, gw = cadeia()
    print("h10 " + h.hex())
    print("dh10/dh0 " + g.hex())
    print("dh10/dw " + " ".join(x.hex() for x in gw))
    print("fim")


if __name__ == "__main__":
    main()
