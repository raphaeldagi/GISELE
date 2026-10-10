"""Rodada 23 do diálogo Python <-> Java: as curvas individuais de esquecimento (a crítica de Anderson e Tweney). Para cada
parte i de 1 a 21, y_i(L) = sim(i, i + L), L = 1..20 (semelhança idf da Rodada 21), sem os L com semelhança zero; os dois
ajustes da Rodada 22 em cada curva. Com `--preparar PASTA`, escreve PASTA/secoes23.txt. Rodar da raiz: python3 dialogo/rodada23.py"""

import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("rodada22", os.path.join(AQUI, "rodada22.py"))
r22 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r22)
r21 = r22.r21


def curvas(cs, ate=20):
    sim = r21.semelhancas(cs)
    res = []
    for i in range(len(cs) - ate):
        ls = [L for L in range(1, ate + 1) if sim[i][i + L] > 0]
        ys = [math.log(sim[i][i + L]) for L in ls]
        _, m1, se = r22.reta([float(L) for L in ls], ys)
        _, m2, sp = r22.reta([math.log(L) for L in ls], ys)
        res.append((cs[i][0], len(ls), -1.0 / m1, se, -m2, sp))
    return res


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "secoes23.txt"), "w", encoding="ascii") as f:
            for n, ws in r21.conjuntos():
                f.write(f"{n}\t{' '.join(ws)}\n")
        return
    pot = 0
    for n, k, tau, se, alfa, sp in curvas(r21.conjuntos()):
        pot += sp < se
        print(f"parte {n}: {k} pontos; tau = {tau.hex()}; residuo exp = {se.hex()}; alfa = {alfa.hex()}; residuo pot = {sp.hex()}")
    print(f"a potencia ganha em {pot}")


if __name__ == "__main__":
    main()
