"""Rodada 22 do diálogo Python <-> Java: a deriva da série tem meia-vida ou memória longa? As médias de semelhança por
distância L = 1..20 (a semelhança idf da Rodada 21), ajustadas por mínimos quadrados em log a uma exponencial
(ln y = a - L/tau) e a uma potência (ln y = b - alfa ln L). Com `--preparar PASTA`, escreve PASTA/secoes22.txt (como a
Rodada 21). Rodar da raiz do repositório: python3 dialogo/rodada22.py"""

import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("rodada21", os.path.join(AQUI, "rodada21.py"))
r21 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r21)


def reta(xs, ys):
    """Mínimos quadrados y = c + m x; devolve (c, m, soma dos quadrados dos resíduos), somas em laço."""
    n = len(xs)
    sx = sy = 0.0
    for x, y in zip(xs, ys):
        sx += x
        sy += y
    mx, my = sx / n, sy / n
    sxy = sxx = 0.0
    for x, y in zip(xs, ys):
        sxy += (x - mx) * (y - my)
        sxx += (x - mx) * (x - mx)
    m = sxy / sxx
    c = my - m * mx
    sse = 0.0
    for x, y in zip(xs, ys):
        e = y - (c + m * x)
        sse += e * e
    return c, m, sse


def deriva(cs, ate=20):
    sim = r21.semelhancas(cs)
    ls = list(range(1, ate + 1))
    ys = [math.log(r21.media_distancia(sim, L)) for L in ls]
    a, m1, sse_exp = reta([float(L) for L in ls], ys)
    b, m2, sse_pot = reta([math.log(L) for L in ls], ys)
    return ys, a, -1.0 / m1, sse_exp, b, -m2, sse_pot


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        sys.argv = [sys.argv[0], "--preparar", sys.argv[2]]
        cs = r21.conjuntos()
        with open(os.path.join(sys.argv[2], "secoes22.txt"), "w", encoding="ascii") as f:
            for n, ws in cs:
                f.write(f"{n}\t{' '.join(ws)}\n")
        return
    ys, a, tau, se, b, alfa, sp = deriva(r21.conjuntos())
    for L, y in enumerate(ys, 1):
        print(f"distancia {L}: ln(media) = {y.hex()}")
    print(f"exponencial: a = {a.hex()}; tau = {tau.hex()}; residuo = {se.hex()}")
    print(f"potencia: b = {b.hex()}; alfa = {alfa.hex()}; residuo = {sp.hex()}")
    print("melhor: " + ("exponencial" if se < sp else "potencia"))


if __name__ == "__main__":
    main()
