"""Rodada 25 do diálogo Python <-> Java: duas memórias (curta e longa) ou uma potência? A curva média da Rodada 22 (L = 1..20)
contra três modelos medidos pelo erro em log: exponencial e potência (k = 2, da Rodada 22) e duas exponenciais
y = A e^(-L/t1) + B e^(-L/t2) (k = 4; grade t1 = 0,25..5, t2 = 2..200, t1 < t2; A, B por mínimos quadrados lineares, só
positivos). AIC = n ln(SSE/n) + 2k. Com `--preparar PASTA`, escreve PASTA/secoes25.txt. Rodar da raiz: python3 dialogo/rodada25.py"""

import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("rodada22", os.path.join(AQUI, "rodada22.py"))
r22 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r22)
r21 = r22.r21


def duas_exponenciais(ys):
    """Melhor (sse em log, A, B, t1, t2) na grade; ys na escala original, L = 1..len(ys)."""
    n = len(ys)
    melhor = None
    for i in range(1, 21):
        t1 = 0.25 * i
        u = [math.exp(-L / t1) for L in range(1, n + 1)]
        for j in range(1, 101):
            t2 = 2.0 * j
            if t1 >= t2:
                continue
            v = [math.exp(-L / t2) for L in range(1, n + 1)]
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
                e = math.log(y) - math.log(A * a + B * b)
                sse += e * e
            if melhor is None or sse < melhor[0]:
                melhor = (sse, A, B, t1, t2)
    return melhor


def aic(sse, n, k):
    return n * math.log(sse / n) + 2 * k


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "secoes25.txt"), "w", encoding="ascii") as f:
            for n, ws in r21.conjuntos():
                f.write(f"{n}\t{' '.join(ws)}\n")
        return
    sim = r21.semelhancas(r21.conjuntos())
    ys = [r21.media_distancia(sim, L) for L in range(1, 21)]
    lys = [math.log(y) for y in ys]
    _, _, se = r22.reta([float(L) for L in range(1, 21)], lys)
    _, _, sp = r22.reta([math.log(L) for L in range(1, 21)], lys)
    s2, A, B, t1, t2 = duas_exponenciais(ys)
    print(f"exponencial: sse = {se.hex()}; aic = {aic(se, 20, 2).hex()}")
    print(f"potencia: sse = {sp.hex()}; aic = {aic(sp, 20, 2).hex()}")
    print(f"duas exponenciais: sse = {s2.hex()}; A = {A.hex()}; B = {B.hex()}; t1 = {t1.hex()}; t2 = {t2.hex()}; aic = {aic(s2, 20, 4).hex()}")
    nomes = [("exponencial", aic(se, 20, 2)), ("potencia", aic(sp, 20, 2)), ("duas exponenciais", aic(s2, 20, 4))]
    m = nomes[0]
    for x in nomes[1:]:
        if x[1] < m[1]:
            m = x
    print("menor aic: " + m[0])


if __name__ == "__main__":
    main()
