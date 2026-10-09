"""Rodada 26 do diálogo Python <-> Java: o método ou a série? As duas exponenciais da Rodada 25 ajustadas EM LOG por
Gauss-Newton: ln y = ln(e^p e^(-L/t1) + e^q e^(-L/t2)), a partir do melhor ponto da grade; 100 iterações; o passo é dividido
por 2 (até 30 vezes) enquanto o erro não cair; o sistema 4x4 por eliminação de Gauss com pivô parcial. Com `--preparar
PASTA`, escreve PASTA/secoes26.txt. Rodar da raiz: python3 dialogo/rodada26.py"""

import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("rodada25", os.path.join(AQUI, "rodada25.py"))
r25 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r25)
r21 = r25.r21


def modelo(th, L):
    p, q, t1, t2 = th
    a = math.exp(p) * math.exp(-L / t1)
    b = math.exp(q) * math.exp(-L / t2)
    return a, b, math.log(a + b)


def erro(th, ly):
    s = 0.0
    for L, y in enumerate(ly, 1):
        e = y - modelo(th, L)[2]
        s += e * e
    return s


def resolver(M, v):
    """Eliminação de Gauss com pivô parcial, n x n."""
    n = len(v)
    A = [M[i][:] + [v[i]] for i in range(n)]
    for c in range(n):
        piv = c
        for r in range(c + 1, n):
            if abs(A[r][c]) > abs(A[piv][c]):
                piv = r
        A[c], A[piv] = A[piv], A[c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            for k in range(c, n + 1):
                A[r][k] -= f * A[c][k]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = A[i][n]
        for k in range(i + 1, n):
            s -= A[i][k] * x[k]
        x[i] = s / A[i][i]
    return x


def gauss_newton(th, ly, iteracoes=100):
    sse = erro(th, ly)
    for _ in range(iteracoes):
        JtJ = [[0.0] * 4 for _ in range(4)]
        Jtr = [0.0] * 4
        for L, y in enumerate(ly, 1):
            a, b, m = modelo(th, L)
            S = a + b
            j = [a / S, b / S, a * (L / (th[2] * th[2])) / S, b * (L / (th[3] * th[3])) / S]
            r = y - m
            for i in range(4):
                Jtr[i] += j[i] * r
                for k in range(4):
                    JtJ[i][k] += j[i] * j[k]
        d = resolver(JtJ, Jtr)
        passo, melhorou = 1.0, False
        for _ in range(30):
            novo = [th[i] + passo * d[i] for i in range(4)]
            if novo[2] > 0.0 and novo[3] > 0.0:
                s2 = erro(novo, ly)
                if s2 < sse:
                    th, sse, melhorou = novo, s2, True
                    break
            passo /= 2.0
        if not melhorou:
            break
    return th, sse


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "secoes26.txt"), "w", encoding="ascii") as f:
            for n, ws in r21.conjuntos():
                f.write(f"{n}\t{' '.join(ws)}\n")
        return
    sim = r21.semelhancas(r21.conjuntos())
    ys = [r21.media_distancia(sim, L) for L in range(1, 21)]
    ly = [math.log(y) for y in ys]
    _, A, B, t1, t2 = r25.duas_exponenciais(ys)
    th, sse = gauss_newton([math.log(A), math.log(B), t1, t2], ly)
    print(f"inicio: sse = {erro([math.log(A), math.log(B), t1, t2], ly).hex()}")
    print(f"em log: A = {math.exp(th[0]).hex()}; B = {math.exp(th[1]).hex()}; t1 = {th[2].hex()}; t2 = {th[3].hex()}; sse = {sse.hex()}")
    print(f"aic = {r25.aic(sse, 20, 4).hex()}; limiar para vencer a potencia = {(0.3095 * math.exp(-0.2)).hex()}")


if __name__ == "__main__":
    main()
