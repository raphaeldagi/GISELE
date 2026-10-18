"""Rodada 77 do diálogo Python <-> Java (Parte 110): o aprendizado contínuo em ℝ² (GD e OGD, duas tarefas de posto 1), bit a bit.
A direção u da tarefa B vem de √ (IEEE, correta nas duas línguas), não de sin/cos (fronteira da Parte 105): θ = 0°, 45°, 60°.
Só +, −, ×, ÷ e √. Da raiz: python3 dialogo/rodada77.py"""
import math

DIRECOES = (("0", 1.0, 0.0), ("45", math.sqrt(0.5), math.sqrt(0.5)), ("60", 0.5, math.sqrt(0.75)))
PASSO, PASSOS = 0.1, 2000


def continuo(u0, u1, ogd):
    w0, w1 = 0.0, 0.0
    for _ in range(PASSOS):
        w0 = w0 - PASSO * (2.0 * (w0 - 1.0))
    a0, a1 = w0, w1
    cb = u0 * a0 + u1 * a1 + 1.0
    for _ in range(PASSOS):
        r = u0 * w0 + u1 * w1 - cb
        g0 = 2.0 * r * u0
        g1 = 2.0 * r * u1
        if ogd:
            g0 = g0 - g0 * 1.0
        w0 = w0 - PASSO * g0
        w1 = w1 - PASSO * g1
    esq = (w0 - 1.0) * (w0 - 1.0)
    rb = u0 * w0 + u1 * w1 - cb
    norma = math.sqrt((w0 - a0) * (w0 - a0) + (w1 - a1) * (w1 - a1))
    return esq, rb * rb, norma


def main():
    for nome, u0, u1 in DIRECOES:
        for ogd in (False, True):
            e, b, n = continuo(u0, u1, ogd)
            print(nome + (" ogd " if ogd else " gd ") + e.hex() + " " + b.hex() + " " + n.hex())
    print("fim")


if __name__ == "__main__":
    main()
