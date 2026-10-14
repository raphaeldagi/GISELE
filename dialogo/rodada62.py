"""Rodada 62 do diálogo Python <-> Java (Parte 95): o passo de atualização do EWC (Elastic Weight Consolidation), bit a bit.
Dado w, w0, a diagonal de Fisher F, uma característica x e um rótulo, calcula o sigmoide `pred = 1/(1+exp(−z))` (z = Σ w·x, com o
EXP PRÓPRIO — o exp é a fronteira da Parte 52), o erro `pred − rótulo`, e atualiza `w_i ← w_i − lr·(erro·x_i + λ·F_i·(w_i−w0_i))`.
O resto é só +−×. Pesos e entrada fixos (determinístico). Rodar da raiz: python3 dialogo/rodada62.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_  # noqa: E402

LR, LAM = 0.025, 0.2
W = [0.4, -0.3, 0.2, 0.1]
W0 = [0.5, -0.2, 0.1, 0.0]
FISHER = [10.0, 0.1, 2.0, 0.5]
X = [1.3, 0.7, 1.0, 1.0]
ROTULO = 1.0


def sigmoide(z):
    zc = max(-15.0, min(15.0, z))
    return 1.0 / (1.0 + exp_(-zc))


def p_cat_inicial():
    z = 0.0
    for i in range(len(W)):
        z = z + W[i] * X[i]
    return sigmoide(z)


def passo_ewc():
    pred = p_cat_inicial()
    erro = pred - ROTULO
    novo = []
    for i in range(len(W)):
        g = erro * X[i] + LAM * FISHER[i] * (W[i] - W0[i])
        novo.append(W[i] - LR * g)
    return novo


def main():
    pred = p_cat_inicial()
    print(f"p_cat {pred.hex()}")
    w = passo_ewc()
    for i in range(len(w)):
        print(f"w {i} {w[i].hex()}")
    print("fim")


if __name__ == "__main__":
    main()
