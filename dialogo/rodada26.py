"""Rodada 26 do diálogo Python <-> Java: o método ou a série? As duas exponenciais da Rodada 25 ajustadas EM LOG por
Gauss-Newton: ln y = ln(e^p e^(-L/t1) + e^q e^(-L/t2)), a partir do melhor ponto da grade; 100 iterações; o passo é dividido
por 2 (até 30 vezes) enquanto o erro não cair; o sistema 4x4 por eliminação de Gauss com pivô parcial. Com `--preparar
PASTA`, escreve PASTA/secoes26.txt. Rodar da raiz: python3 dialogo/rodada26.py

O exp e o log são PRÓPRIOS (exp_ e log_): os da libm do Python (glibc) e do Java diferem em 0,29% e 0,07% dos argumentos, e a
primeira versão desta rodada deu DIFERENTES (guardada em dialogo/registro/). Só +, −, ×, ÷ e escalas exatas por 2^k."""

import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("rodada25", os.path.join(AQUI, "rodada25.py"))
r25 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r25)
r21 = r25.r21


LN2_HI = 6.93147180369123816490e-01  # ln 2 em duas partes (como na fdlibm): k·LN2_HI é exato para |k| < 2^20
LN2_LO = 1.90821492927058770002e-10
SQRT2 = 1.4142135623730951


def exp_(x):
    """e^x = 2^k · e^r, k = arredondar(x/ln 2), r = x − k ln 2 (|r| ≤ 0,35); e^r pela série de Taylor (Horner, 22 termos)."""
    k = math.floor(x / (LN2_HI + LN2_LO) + 0.5)
    r = (x - k * LN2_HI) - k * LN2_LO
    p = 1.0
    for i in range(22, 0, -1):
        p = 1.0 + r * p / i
    return math.ldexp(p, int(k))


def log_(x):
    """ln x = e ln 2 + ln m, x = m · 2^e com m em [√½, √2); ln m = 2 atanh s = 2 s Σ s^(2j)/(2j+1), s = (m − 1)/(m + 1)."""
    m, e = math.frexp(x)
    m, e = m * 2.0, e - 1
    if m > SQRT2:
        m, e = m / 2.0, e + 1
    s = (m - 1.0) / (m + 1.0)
    s2 = s * s
    p = 1.0 / 41.0
    for j in range(19, -1, -1):
        p = 1.0 / (2 * j + 1) + s2 * p
    return e * LN2_HI + (e * LN2_LO + 2.0 * s * p)


def modelo(th, L):
    p, q, t1, t2 = th
    a = exp_(p) * exp_(-L / t1)
    b = exp_(q) * exp_(-L / t2)
    return a, b, log_(a + b)


def grade(ys):
    """A grade da Rodada 25 (rodada25.duas_exponenciais), com exp_ e log_ próprios."""
    n = len(ys)
    melhor = None
    for i in range(1, 21):
        t1 = 0.25 * i
        u = [exp_(-L / t1) for L in range(1, n + 1)]
        for j in range(1, 101):
            t2 = 2.0 * j
            if t1 >= t2:
                continue
            v = [exp_(-L / t2) for L in range(1, n + 1)]
            suu = svv = suv = suy = svy = 0.0
            for a, b, y in zip(u, v, ys):
                suu += a * a
                svv += b * b
                suv += a * b
                suy += a * y
                svy += b * y
            det = suu * svv - suv * suv
            if det == 0.0:
                continue
            A = (suy * svv - svy * suv) / det
            B = (svy * suu - suy * suv) / det
            if A <= 0.0 or B <= 0.0:
                continue
            sse = 0.0
            for a, b, y in zip(u, v, ys):
                e = log_(y) - log_(A * a + B * b)
                sse += e * e
            if melhor is None or sse < melhor[0]:
                melhor = (sse, A, B, t1, t2)
    return melhor


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
    ly = [log_(y) for y in ys]
    _, A, B, t1, t2 = grade(ys)
    th, sse = gauss_newton([log_(A), log_(B), t1, t2], ly)
    print(f"inicio: sse = {erro([log_(A), log_(B), t1, t2], ly).hex()}")
    print(f"em log: A = {exp_(th[0]).hex()}; B = {exp_(th[1]).hex()}; t1 = {th[2].hex()}; t2 = {th[3].hex()}; sse = {sse.hex()}")
    print(f"aic = {(20 * log_(sse / 20) + 8).hex()}; limiar para vencer a potencia = {(0.3095 * exp_(-0.2)).hex()}")


if __name__ == "__main__":
    main()
